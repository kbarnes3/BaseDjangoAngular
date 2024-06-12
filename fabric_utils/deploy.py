from typing import Optional

from colorama import Fore, init
from fabric import Task
from fabric.connection import Connection
from plush.patchwork.files import exists as patchwork_exists
from plush.fabric_commands.permissions import ensure_directory, set_permissions_file

CONFIGURATIONS = {
    'daily': {
        'branch': 'trunk',
        'ssl': True,
        'secret_repo_name': 'kbarnes3/BaseDjangoAngularSecrets',
        'secret_repo_branch': 'trunk',
    },
    'dev': {
        'branch': 'trunk',
        'ssl': True,
        'secret_repo_name': 'kbarnes3/BaseDjangoAngularSecrets',
        'secret_repo_branch': 'trunk',
    },
    'prod': {
        'branch': 'prod',
        'ssl': True,
        'secret_repo_name': 'kbarnes3/BaseDjangoAngularSecrets',
        'secret_repo_branch': 'trunk',
    },
    'staging': {
        'branch': 'prod',
        'ssl': True,
        'secret_repo_name': 'kbarnes3/BaseDjangoAngularSecrets',
        'secret_repo_branch': 'trunk',
    },
}

PYTHON_DIR = '/var/www/python'
WEBADMIN_GROUP = 'webadmin'

init(autoreset=True)

class AllowedException(Exception):
    pass


def exists(conn: Connection, path: str) -> bool:
    # pylint doesn't understand the @set_runner decorator
    # create a wrapper so we only have to suppress the error once
    return patchwork_exists(conn, path) # pylint: disable=E1120

def get_repo_dir(config: str) -> str:
    return f'{PYTHON_DIR}/newdjangosite-{config}'


def get_backend_dir(repo_dir: str) -> str:
    return f'{repo_dir}/back'


def get_frontend_dir(repo_dir: str) -> str:
    return f'{repo_dir}/front'


def get_virtualenv_python_bin(repo_dir: str) -> str:
    return f'{repo_dir}/venv/bin/python'


def get_secret_repo_dir(config: str) -> str:
    return f'{PYTHON_DIR}/newdjangosite-{config}-secrets'


def get_secret_repo_name(config: str) -> str:
    configuration = CONFIGURATIONS[config]
    return configuration['secret_repo_name']


def get_secret_repo_branch(config: str, branch_override: Optional[str] = None) -> str:
    if branch_override:
        return branch_override

    configuration = CONFIGURATIONS[config]
    return configuration['secret_repo_branch']


@Task
def deploy(conn, config, branch=None, secret_branch=None):
    configuration = CONFIGURATIONS[config]
    if not branch:
        branch = configuration['branch']
    secret_branch = get_secret_repo_branch(config, secret_branch)
    use_ssl = configuration['ssl']

    print(Fore.GREEN + f'Deploying {config} from branch {branch} with ' +
                        f'secret repo from branch {secret_branch}')

    repo_dir = get_repo_dir(config)
    config_dir = f'{repo_dir}/config/ubuntu-24.04'
    daily_scripts_dir = f'{config_dir}/cron.daily'
    uwsgi_dir = f'{config_dir}/uwsgi'
    nginx_dir = f'{config_dir}/nginx'
    secret_repo_dir = get_secret_repo_dir(config)
    ssl_dir = f'{secret_repo_dir}/{config}/ssl'

    _update_source(conn, repo_dir, branch)
    _update_source(conn, secret_repo_dir, secret_branch)
    update_backend_dependencies(conn, repo_dir)
    _compile_source(conn, config, repo_dir)
    _update_scripts(conn, config, daily_scripts_dir)
    _update_database(conn, config, repo_dir)
    _reload_code(conn, config, uwsgi_dir)
    _build_content(conn, repo_dir)
    _reload_web(conn, config, nginx_dir, use_ssl, ssl_dir)
    _run_tests(conn, config, repo_dir)

    print(Fore.GREEN + f'Deployment to {config} complete')


def _update_source(conn: Connection, repo_dir: str, branch: str):
    print(Fore.GREEN + f'update_source for {repo_dir}')
    ensure_directory(conn, repo_dir, owning_group=WEBADMIN_GROUP, mod='ug+w')
    with conn.cd(repo_dir):
        conn.run('sudo git fetch origin')
        conn.run(f'sudo git reset --hard origin/{branch}')


def update_backend_dependencies(conn: Connection, repo_dir: str):
    print(Fore.GREEN + 'update_backend_dependencies')

    venv_dir = f'{repo_dir}/venv'
    if not exists(conn, venv_dir):
        print(Fore.GREEN + 'Creating virtualenv')
        conn.run(f'python3 -m venv --system-site-packages {venv_dir}')

    with conn.cd(repo_dir):
        print(Fore.GREEN + 'Updating pip')
        conn.run('venv/bin/python -m pip install --upgrade pip')

        print(Fore.GREEN + 'Updating pip-tools')
        conn.run('venv/bin/python -m pip install --upgrade pip-tools')

        print(Fore.GREEN + 'Installing dependencies with pip-sync')
        conn.run('venv/bin/pip-sync ubuntu64-py312-requirements.txt')


def _compile_source(conn: Connection,
                    config: str,
                    repo_dir: str):
    print(Fore.GREEN + 'compile_source')
    backend_dir = get_backend_dir(repo_dir)
    python_bin = get_virtualenv_python_bin(repo_dir)

    with conn.cd(backend_dir):
        conn.run('sudo find . -iname "*.pyc" -delete')
        conn.run(f'sudo {python_bin} -m compileall .')
        conn.run(f'sudo {python_bin} manage_{config}.py collectstatic --noinput')


def _update_scripts(conn: Connection, config: str, daily_scripts_dir: str):
    print(Fore.GREEN + 'update_scripts')
    cron_daily_dir = '/etc/cron.daily'
    with conn.cd(daily_scripts_dir):
        conn.run(f'sudo cp newdjangosite-{config}-* {cron_daily_dir}')

    with conn.cd(cron_daily_dir):
        conn.run(f'sudo chmod 755 newdjangosite-{config}-*')


def _update_database(conn: Connection, config: str, repo_dir: str):
    print(Fore.GREEN + 'update_database')
    backend_dir = get_backend_dir(repo_dir)
    python_bin = get_virtualenv_python_bin(repo_dir)
    with conn.cd(backend_dir):
        conn.run(f'sudo {python_bin} manage_{config}.py migrate')


def _reload_code(conn: Connection, config: str, uwsgi_dir: str):
    print(Fore.GREEN + 'reload_code')
    with conn.cd(uwsgi_dir):
        conn.run(f'sudo cp newdjangosite-{config}.ini /etc/uwsgi/apps-available')
        conn.run(f'sudo chmod 644 /etc/uwsgi/apps-available/newdjangosite-{config}.ini')
        conn.run(f'sudo systemctl enable uwsgi-app@newdjangosite-{config}.socket')
        conn.run(f'sudo systemctl enable uwsgi-app@newdjangosite-{config}.service')
        conn.run(f'sudo systemctl start uwsgi-app@newdjangosite-{config}.socket')
        conn.run(f'sudo touch /var/uwsgi/newdjangosite-{config}.reload')


def _build_content(conn: Connection, repo_dir: str):
    angular_dir = get_frontend_dir(repo_dir)
    print(Fore.GREEN + 'build_content')
    with conn.cd(angular_dir):
        conn.run('sudo npm install --location=global npm@8')
        conn.run('sudo npm install --location=global @angular/cli')
        conn.run('sudo npm ci')
        conn.run('sudo npm run-script build')
        conn.run('sudo rsync -va dist/front built')


def _reload_web(conn: Connection, config: str, nginx_dir: str, ssl: bool, ssl_dir: str):
    print(Fore.GREEN + 'reload_web')
    with conn.cd(nginx_dir):
        conn.run(f'sudo cp {config}.yourdomain.tld /etc/nginx/sites-enabled/')

    if ssl:
        with conn.cd(ssl_dir):
            conn.run(f'sudo cp {config}.yourdomain.tld.* /etc/nginx/ssl')
            conn.run(f'sudo chown root /etc/nginx/ssl/{config}.yourdomain.tld.*')
            conn.run(f'sudo chgrp root /etc/nginx/ssl/{config}.yourdomain.tld.*')
            conn.run(f'sudo chmod 644 /etc/nginx/ssl/{config}.yourdomain.tld.*')

    conn.sudo('/etc/init.d/nginx reload')


def _run_tests(conn: Connection, config: str, repo_dir: str):
    print(Fore.GREEN + 'run_tests')
    backend_dir = get_backend_dir(repo_dir)
    python_bin = get_virtualenv_python_bin(repo_dir)
    with conn.cd(backend_dir):
        conn.run(f'{python_bin} manage_{config}.py test')


def checkout_branch(conn: Connection, repo_dir: str, config: str, branch: Optional[str] = None):
    if not branch:
        configuration = CONFIGURATIONS[config]
        branch = configuration['branch']

    _update_source(conn, repo_dir, branch)


@Task
def deploy_global_config(conn, config):
    print(Fore.GREEN + 'deploy_global_config')
    repo_dir = get_repo_dir(config)
    global_dir = f'{repo_dir}/config/ubuntu-24.04/global'
    nginx_conf = '/etc/nginx/nginx.conf'
    uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
    uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'

    conn.sudo(f'cp {global_dir}/nginx.conf {nginx_conf}')
    set_permissions_file(conn, nginx_conf, 'root', 'root', '644')

    conn.sudo(f'cp {global_dir}/uwsgi-app@.socket {uwsgi_socket}')
    set_permissions_file(conn, uwsgi_socket, 'root', 'root', '644')

    conn.sudo(f'cp {global_dir}/uwsgi-app@.service {uwsgi_service}')
    set_permissions_file(conn, uwsgi_service, 'root', 'root', '644')

    conn.sudo('/etc/init.d/nginx restart')
    print(Fore.GREEN + 'deploy_global_config done')


@Task
def shutdown(conn, config, branch=None, secret_branch=None):
    configuration = CONFIGURATIONS[config]
    if not branch:
        branch = configuration['branch']
    secret_branch = get_secret_repo_branch(config, secret_branch)
    use_ssl = configuration['ssl']

    print(Fore.GREEN + ('Shuting down {0} from branch {1} with ' +
                        'secret repro from branch {2}').format(
                            config, branch, secret_branch))

    repo_dir = get_repo_dir(config)
    nginx_dir = f'{repo_dir}/config/ubuntu-24.04/nginx/shutdown'
    secret_repo_dir = get_secret_repo_dir(config)
    ssl_dir = f'{secret_repo_dir}/{config}/ssl'

    _update_source(conn, repo_dir, branch)
    _update_source(conn, secret_repo_dir, secret_branch)
    _reload_web(conn, config, nginx_dir, use_ssl, ssl_dir)
    print(Fore.GREEN + 'Static shutdown site deployed')
