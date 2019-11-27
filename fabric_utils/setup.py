from importlib import import_module

from fabric import Task
from fabric.connection import Connection
from patchwork.files import directory, exists
import plush.fabric_commands
from plush.fabric_commands.git import clone
from plush.fabric_commands.permissions import set_permissions_file
from plush.fabric_commands.ssh_key import create_key
from plush.oauth_flow import verify_access_token
from plush.repo_keys import add_repo_key

from .deploy import AllowedException, checkout_branch, deploy, get_repo_dir, WEBADMIN_GROUP

REPO_FULL_NAME = 'GitHubUser/GitHubRepo'


@Task
def setup_user(conn, user, no_sudo_passwd=False, public_key_file=None):
    messages = plush.fabric_commands.prepare_user(
        conn,
        user,
        WEBADMIN_GROUP,
        add_sudo=True,
        no_sudo_passwd=no_sudo_passwd)
    add_authorized_key(conn, user, public_key_file)

    if not exists(conn, '/usr/bin/createuser'):
        plush.fabric_commands.install_packages(conn, ['postgresql'])

    matching_user_count = conn.sudo(
        "psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='{0}'\"".format(user),
        user='postgres').stdout
    if '1' not in matching_user_count:
        conn.sudo('createuser -s {0}'.format(user), user='postgres')

    if messages:
        print("========================================")
        print(messages)
        print("========================================")


@Task
def add_authorized_key(conn, user, public_key_file):
    if public_key_file:
        with open(public_key_file, 'r') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(conn, user, public_key_contents)


@Task
def disable_ssh_passwords(conn):
    sshd_config = '/etc/ssh/sshd_config'
    conn.sudo("sed -i '/^ *PasswordAuthentication/d' {0}".format(sshd_config))
    conn.sudo('echo "PasswordAuthentication no" | sudo tee -a {0}'.format(sshd_config), pty=True)
    print("========================================")
    print("Password authentication disabled for SSH.")
    print("Restart the SSH daemon by logging into the console and running:")
    print("sudo service ssh restart")
    print("Alternatively, reboot the server if console access isn't readily available.")
    print("========================================")


@Task
def setup_server(conn, setup_wins=False):
    conn.sudo('add-apt-repository universe')
    conn.sudo('apt-get update')

    _setup_node(conn)

    base_packages = [
        'git',
        'python3-venv',
        'postgresql',
        'python3-psycopg2',
        'nginx',
        'uwsgi',
        'uwsgi-plugin-python3',
    ]

    plush.fabric_commands.install_packages(conn, base_packages)

    if setup_wins:
        _setup_wins(conn)

    conn.sudo('mkdir -p /etc/nginx/ssl')
    directory(conn, '/var/www', group=WEBADMIN_GROUP, sudo=True)
    directory(conn, '/var/www/python', group=WEBADMIN_GROUP, sudo=True)

    matching_user_count = conn.run(
        "psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='root'\"").stdout
    if '1' not in matching_user_count:
        conn.run('createuser -s root')

    directory(conn, '/var/uwsgi', user='root', group='root', mode='777', sudo=True)

    default_site = '/etc/nginx/sites-enabled/default'
    if exists(conn, default_site):
        conn.sudo('rm {0}'.format(default_site))
    conn.sudo('/etc/init.d/nginx start')


def _setup_node(conn: Connection):
    conn.sudo('curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -', pty=True)
    conn.sudo('apt-get update')
    plush.fabric_commands.install_packages(conn, ['nodejs'])


def _setup_wins(conn: Connection):
    wins_packages = [
        'samba',
        'smbclient',
        'winbind',
    ]

    plush.fabric_commands.install_packages(conn, wins_packages)
    sudo('sed -i s/\'hosts:.*/hosts:          files dns wins/\' /etc/nsswitch.conf')
    resolved_config = '/etc/systemd/resolved.conf'
    conn.sudo("sed -i '/^ *Domains/d' {0}".format(resolved_config))
    conn.sudo('echo "Domains=localdomain" | sudo tee -a {0}'.format(resolved_config), pty=True)
    conn.sudo('service systemd-resolved restart')


def setup_deployment(config, branch=''):
    django_settings = import_module('newdjangosite.settings_{0}'.format(config))
    db_settings = django_settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    repo_dir = get_repo_dir(config)

    database_created = False
    with settings(abort_exception=AllowedException):
        try:
            run(
                ('createdb '
                 '--encoding=UTF8 '
                 '--locale=en_US.UTF-8 '
                 '--owner=postgres '
                 '--template=template0 {0}').format(db_name))
            database_created = True
        except AllowedException:
            pass

    with settings(abort_exception=AllowedException):
        try:
            run('createuser -d -R -S {0}'.format(db_user))
        except AllowedException:
            pass

    run('psql -d postgres -c \"ALTER ROLE {0} WITH ENCRYPTED PASSWORD \'{1}\';\"'.format(
        db_user,
        db_password))

    _setup_repo(repo_dir)
    checkout_branch(repo_dir, config, branch)

    with cd(repo_dir):
        if not exists('venv'):
            run('python3 -m venv --system-site-packages venv')

    global_dir = '{0}/config/ubuntu-18.04/global'.format(repo_dir)
    with cd(global_dir):
        uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
        uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'

        if not exists(uwsgi_socket):
            sudo('cp uwsgi-app@.socket {0}'.format(uwsgi_socket))
            set_permissions_file(uwsgi_socket, 'root', 'root', '644')

        if not exists(uwsgi_service):
            sudo('cp uwsgi-app@.service {0}'.format(uwsgi_service))
            set_permissions_file(uwsgi_service, 'root', 'root', '644')

    deploy(config, branch)

    if database_created:
        with cd(repo_dir):
            run('venv/bin/python web/manage_{0}.py createsuperuser'.format(config))


def _setup_repo(repo_dir):
    make_directory(WEBADMIN_GROUP, repo_dir)

    if not exists('{0}/.git'.format(repo_dir)):
        if not verify_access_token():
            raise Exception('Unable to access GitHub account')
        create_key(REPO_FULL_NAME, WEBADMIN_GROUP)
        add_repo_key(REPO_FULL_NAME)
        clone(REPO_FULL_NAME, repo_dir)
