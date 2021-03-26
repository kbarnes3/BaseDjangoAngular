from importlib import import_module
from typing import Optional

from fabric import Task
from fabric.connection import Connection
from patchwork.files import directory, exists
import plush.fabric_commands
from plush.fabric_commands.git import clone
from plush.fabric_commands.permissions import set_permissions_file
from plush.fabric_commands.ssh_key import create_key
from plush.oauth_flow import verify_access_token
from plush.repo_keys import add_repo_key

from .deploy import checkout_branch, deploy, get_secret_repo_branch, get_secret_repo_dir
from .deploy import get_secret_repo_name, get_repo_dir, WEBADMIN_GROUP

REPO_FULL_NAME = 'kbarnes3/BaseDjangoAngular'


@Task
def setup_user(conn, user, disable_sudo_passwd=False, set_public_key_file=None):
    messages = plush.fabric_commands.prepare_user(
        conn,
        user,
        WEBADMIN_GROUP,
        add_sudo=True,
        no_sudo_passwd=disable_sudo_passwd)
    add_authorized_key(conn, user, set_public_key_file)

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
def add_authorized_key(conn, user, set_public_key_file):
    if set_public_key_file:
        with open(set_public_key_file, 'r') as public_key:
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
    conn.sudo('sed -i s/\'hosts:.*/hosts:          files dns wins/\' /etc/nsswitch.conf')
    resolved_config = '/etc/systemd/resolved.conf'
    conn.sudo("sed -i '/^ *Domains/d' {0}".format(resolved_config))
    conn.sudo('echo "Domains=localdomain" | sudo tee -a {0}'.format(resolved_config), pty=True)
    conn.sudo('service systemd-resolved restart')


@Task
def setup_deployment(conn, config, branch=None, secret_branch=None):
    django_settings = import_module('back.newdjangosite.settings_{0}'.format(config))
    db_settings = django_settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    repo_dir = get_repo_dir(config)

    # database_created = False
    database_exists_count = conn.run(
        "psql postgres -tAc \"SELECT 1 FROM pg_catalog.pg_database WHERE datname='{0}'\"".format(db_name)).stdout
    if '1' not in database_exists_count:
        conn.run(
            ('createdb '
             '--encoding=UTF8 '
             '--locale=en_US.UTF-8 '
             '--owner=postgres '
             '--template=template0 {0}').format(db_name))
        # database_created = True

    matching_user_count = conn.run(
        "psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='{0}'\"".format(db_user)).stdout
    if '1' not in matching_user_count:
        conn.run('createuser -s {0}'.format(db_user))

    conn.run('psql -d postgres -c \"ALTER ROLE {0} WITH ENCRYPTED PASSWORD \'{1}\';\"'.format(
        db_user,
        db_password))

    _setup_main_repo(conn, repo_dir, config, branch)
    _setup_secret_repo(conn, config, secret_branch)

    venv_dir = '{0}/venv'.format(repo_dir)
    if not exists(conn, venv_dir):
        conn.sudo('python3 -m venv --system-site-packages {0}'.format(venv_dir))


    global_dir = '{0}/config/ubuntu-18.04/global'.format(repo_dir)
    uwsgi_socket_source = '{0}/uwsgi-app@.socket'.format(global_dir)
    uwsgi_service_source = '{0}/uwsgi-app@.service'.format(global_dir)

    uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
    uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'

    if not exists(conn, uwsgi_socket):
        conn.sudo('cp {0} {1}'.format(uwsgi_socket_source, uwsgi_socket))
        set_permissions_file(conn, uwsgi_socket, 'root', 'root', '644')

    if not exists(conn, uwsgi_service):
        conn.sudo('cp {0} {1}'.format(uwsgi_service_source, uwsgi_service))
        set_permissions_file(conn, uwsgi_service, 'root', 'root', '644')

    print('deploying...')
    deploy(conn, config, branch, secret_branch)

    # if database_created:
        # with cd(repo_dir):
            # run('venv/bin/python web/manage_{0}.py createsuperuser'.format(config))


def _setup_main_repo(conn: Connection, repo_dir: str, config: str, branch: Optional[str] = None):
    _setup_repo(conn, repo_dir, REPO_FULL_NAME)
    checkout_branch(conn, repo_dir, config, branch)


def _setup_secret_repo(conn: Connection, config: str, secret_branch_override: Optional[str] = None):
    secret_repo_dir = get_secret_repo_dir(config)
    secret_repo_name = get_secret_repo_name(config)
    secret_branch = get_secret_repo_branch(config, secret_branch_override)

    _setup_repo(conn, secret_repo_dir, secret_repo_name)
    checkout_branch(conn, secret_repo_dir, config, secret_branch)


def _setup_repo(conn: Connection, repo_dir: str, repo_name: str):
    directory(conn, repo_dir, group=WEBADMIN_GROUP, sudo=True)

    if not exists(conn, '{0}/.git'.format(repo_dir)):
        if not verify_access_token():
            raise Exception("Unable to access GitHub account. Run 'auth' to fix this")
        create_key(conn, repo_name, WEBADMIN_GROUP)
        add_repo_key(conn, repo_name)
        clone(conn, repo_name, repo_dir, skip_strict_key_checking=True)
