from typing import Optional

from colorama import Fore, init as colorama_init
from fabric import Task
from fabric.connection import Connection
import plush.fabric_commands
from plush.fabric_commands.git import clone
from plush.fabric_commands.permissions import ensure_directory, set_permissions_file
from plush.fabric_commands.ssh_key import create_key
from plush.oauth_flow import verify_access_token
from plush.repo_keys import add_repo_key

from .deploy import checkout_branch, deploy, exists, get_secret_repo_branch
from .deploy import get_secret_repo_dir, get_secret_repo_name, get_repo_dir
from .deploy import update_backend_dependencies, WEBADMIN_GROUP

REPO_FULL_NAME = 'kbarnes3/BaseDjangoAngular'
colorama_init(autoreset=True)


@Task
def setup_user(conn, user, disable_sudo_passwd=False, set_public_key_file=None):
    print(Fore.GREEN + f'Configuring {user}')
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
        f"psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='{user}'\"",
        user='postgres').stdout
    if '1' not in matching_user_count:
        conn.sudo(f'createuser -s {user}', user='postgres')

    if messages:
        print("========================================")
        print(messages)
        print("========================================")
    print(Fore.GREEN + f'{user} configured')


@Task
def add_authorized_key(conn, user, set_public_key_file):
    if set_public_key_file:
        with open(set_public_key_file, 'r', encoding='utf-8') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(conn, user, public_key_contents)


@Task
def disable_ssh_passwords(conn):
    sshd_config = '/etc/ssh/sshd_config'
    sshd_config_dir = '/etc/ssh/sshd_config.d/'
    conn.sudo(f"sed -i '/^ *PasswordAuthentication/d' {sshd_config}")
    conn.sudo(f"find {sshd_config_dir} -type f -execdir " +
              "sed -i '/^ *PasswordAuthentication/d' {} \\;")
    conn.sudo(f'echo "PasswordAuthentication no" | sudo tee -a {sshd_config}', pty=True)
    print("========================================")
    print("Password authentication disabled for SSH.")
    print("Restart the SSH daemon by logging into the console and running:")
    print("sudo service ssh restart")
    print("Alternatively, reboot the server if console access isn't readily available.")
    print("========================================")


@Task
def setup_server(conn):
    print(Fore.GREEN + 'Starting server setup')
    conn.sudo('add-apt-repository universe')
    conn.sudo('apt-get update')

    _setup_node(conn)

    base_packages = [
        'git',
        'python3-venv',
        'postgresql',
        'nginx',
        'uwsgi',
        'uwsgi-plugin-python3',
    ]

    plush.fabric_commands.install_packages(conn, base_packages)

    conn.sudo('mkdir -p /etc/nginx/ssl')
    ensure_directory(conn, '/var/www', owning_group=WEBADMIN_GROUP)
    ensure_directory(conn, '/var/www/python', owning_group=WEBADMIN_GROUP)

    matching_user_count = conn.run(
        "psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='root'\"").stdout
    if '1' not in matching_user_count:
        conn.run('createuser -s root')

    ensure_directory(conn, '/var/uwsgi', owning_group='root', mod='777')

    default_site = '/etc/nginx/sites-enabled/default'
    if exists(conn, default_site):
        conn.sudo(f'rm {default_site}')
    conn.sudo('/etc/init.d/nginx start')
    print(Fore.GREEN + 'Server setup done')


def _setup_node(conn: Connection):
    conn.sudo('curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -', pty=True)
    conn.sudo('apt-get update')
    plush.fabric_commands.install_packages(conn, ['nodejs'])


@Task
def setup_deployment(conn, config, branch=None, secret_branch=None):
    print(Fore.GREEN + f'Starting setup deployment for {config}')
    repo_dir = get_repo_dir(config)

    print(Fore.GREEN + 'Cloning main repo')
    _setup_main_repo(conn, repo_dir, config, branch)
    print(Fore.GREEN + 'Cloning secret repo')
    _setup_secret_repo(conn, config, secret_branch)

    update_backend_dependencies(conn, repo_dir)

    with conn.cd(repo_dir):
        print(Fore.GREEN + 'Creating database and user')
        conn.run(f'venv/bin/python back/create_db.py {config}')


    global_dir = f'{repo_dir}/config/ubuntu-24.04/global'
    uwsgi_socket_source = f'{global_dir}/uwsgi-app@.socket'
    uwsgi_service_source = f'{global_dir}/uwsgi-app@.service'

    uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
    uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'


    print(Fore.GREEN + 'Configuring UWSGI')
    if not exists(conn, uwsgi_socket):
        conn.sudo(f'cp {uwsgi_socket_source} {uwsgi_socket}')
        set_permissions_file(conn, uwsgi_socket, 'root', 'root', '644')

    if not exists(conn, uwsgi_service):
        conn.sudo(f'cp {uwsgi_service_source} {uwsgi_service}')
        set_permissions_file(conn, uwsgi_service, 'root', 'root', '644')

    print(Fore.GREEN + 'Deploying')
    deploy(conn, config, branch, secret_branch)
    print(Fore.GREEN + f'Setup deployment done for {config}')


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
    ensure_directory(conn, repo_dir, owning_group=WEBADMIN_GROUP)

    if not exists(conn, f'{repo_dir}/.git'):
        if not verify_access_token():
            raise PermissionError("Unable to access GitHub account. Run 'auth' to fix this")
        create_key(conn, repo_name, WEBADMIN_GROUP)
        add_repo_key(conn, repo_name)
        clone(conn, repo_name, repo_dir, skip_strict_key_checking=True)

    conn.sudo(f'git config --system --add safe.directory {repo_dir}')


@Task
def setup_superuser(conn, config, email, given_name, surname, password): # pylint: disable=R0913
    print(Fore.GREEN + f'Setting up new superuser for {config} deployment')
    repo_dir = get_repo_dir(config)

    env = {'DJANGO_SUPERUSER_PASSWORD': password}

    with conn.cd(repo_dir):
        conn.run(f'venv/bin/python back/manage_{config}.py createsuperuser --no-input ' +
                  f'--primary_email {email} --given_name {given_name} --surname {surname}',
                  env=env)
