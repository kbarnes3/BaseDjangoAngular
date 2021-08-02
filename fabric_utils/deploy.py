from typing import Optional
from fabric import Task
from fabric.connection import Connection
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


class AllowedException(Exception):
    pass


def get_repo_dir(config: str) -> str:
    return '{0}/newdjangosite-{1}'.format(PYTHON_DIR, config)


def get_secret_repo_dir(config: str) -> str:
    return '{0}/newdjangosite-{1}-secrets'.format(PYTHON_DIR, config)


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

    repo_dir = get_repo_dir(config)
    backend_dir = '{0}/back'.format(repo_dir)
    frontend_dir = '{0}/front'.format(repo_dir)
    config_dir = '{0}/config/ubuntu-18.04'.format(repo_dir)
    daily_scripts_dir = '{0}/cron.daily'.format(config_dir)
    uwsgi_dir = '{0}/uwsgi'.format(config_dir)
    nginx_dir = '{0}/nginx'.format(config_dir)
    virtualenv_python = '{0}/venv/bin/python'.format(repo_dir)
    secret_repo_dir = get_secret_repo_dir(config)
    ssl_dir = '{0}/{1}/ssl'.format(secret_repo_dir, config)

    _update_source(conn, repo_dir, branch)
    _update_source(conn, secret_repo_dir, secret_branch)
    _compile_source(conn, config, repo_dir, backend_dir, virtualenv_python)
    _update_scripts(conn, config, daily_scripts_dir)
    _update_database(conn, config, backend_dir, virtualenv_python)
    _reload_code(conn, config, uwsgi_dir)
    _build_content(conn, frontend_dir)
    _reload_web(conn, config, nginx_dir, use_ssl, ssl_dir)
    _run_tests(conn, config, backend_dir, virtualenv_python)


def _update_source(conn: Connection, repo_dir: str, branch: str):
    ensure_directory(conn, repo_dir, owning_group=WEBADMIN_GROUP, mod='ug+w')
    with conn.cd(repo_dir):
        conn.run('sudo git fetch origin')
        conn.run('sudo git reset --hard origin/{0}'.format(branch))


def _compile_source(conn: Connection, config: str, repo_dir: str, backend_dir: str, virtualenv_python: str):
    print('compile_source')
    with conn.cd(repo_dir):
        conn.run('venv/bin/pip install --quiet --requirement=requirements.txt')

    with conn.cd(backend_dir):
        conn.run('sudo find . -iname "*.pyc" -delete')
        conn.run('sudo {0} -m compileall .'.format(virtualenv_python))
        conn.run('sudo {0} manage_{1}.py collectstatic --noinput'.format(virtualenv_python, config))


def _update_scripts(conn: Connection, config: str, daily_scripts_dir: str):
    print('update_scripts')
    cron_daily_dir = '/etc/cron.daily'
    with conn.cd(daily_scripts_dir):
        conn.run('sudo cp newdjangosite-{0}-* {1}'.format(config, cron_daily_dir))

    with conn.cd(cron_daily_dir):
        conn.run('sudo chmod 755 newdjangosite-{0}-*'.format(config))


def _update_database(conn: Connection, config: str, backend_dir: str, virtualenv_python: str):
    print('update_database')
    with conn.cd(backend_dir):
        conn.run('sudo {0} manage_{1}.py migrate'.format(virtualenv_python, config))


def _reload_code(conn: Connection, config: str, uwsgi_dir: str):
    print('reload_code')
    with conn.cd(uwsgi_dir):
        conn.run('sudo cp newdjangosite-{0}.ini /etc/uwsgi/apps-available'.format(config))
        conn.run('sudo chmod 644 /etc/uwsgi/apps-available/newdjangosite-{0}.ini'.format(config))
        conn.run('sudo systemctl enable uwsgi-app@newdjangosite-{0}.socket'.format(config))
        conn.run('sudo systemctl enable uwsgi-app@newdjangosite-{0}.service'.format(config))
        conn.run('sudo systemctl start uwsgi-app@newdjangosite-{0}.socket'.format(config))
        conn.run('sudo touch /var/run/uwsgi/newdjangosite-{0}.reload'.format(config))


def _build_content(conn: Connection, angular_dir: str):
    print('build_content')
    with conn.cd(angular_dir):
        conn.run('sudo npm install -g npm@7')
        conn.run('sudo npm install -g @angular/cli')
        conn.run('sudo npm ci')
        conn.run('sudo npm run-script build')


def _reload_web(conn: Connection, config: str, nginx_dir: str, ssl: bool, ssl_dir: str):
    print('reload_web')
    with conn.cd(nginx_dir):
        conn.run('sudo cp {0}.yourdomain.tld /etc/nginx/sites-enabled/'.format(config))

    if ssl:
        with conn.cd(ssl_dir):
            conn.run('sudo cp {0}.yourdomain.tld.* /etc/nginx/ssl'.format(config))
            conn.run('sudo chown root /etc/nginx/ssl/{0}.yourdomain.tld.*'.format(config))
            conn.run('sudo chgrp root /etc/nginx/ssl/{0}.yourdomain.tld.*'.format(config))
            conn.run('sudo chmod 644 /etc/nginx/ssl/{0}.yourdomain.tld.*'.format(config))

    conn.sudo('/etc/init.d/nginx reload')


def _run_tests(conn: Connection, config: str, backend_dir: str, virtualenv_python: str):
    print('run_tests')
    with conn.cd(backend_dir):
        conn.run('{0} manage_{1}.py test'.format(virtualenv_python, config))


def checkout_branch(conn: Connection, repo_dir: str, config: str, branch: Optional[str] = None):
    if not branch:
        configuration = CONFIGURATIONS[config]
        branch = configuration['branch']

    _update_source(conn, repo_dir, branch)


def deploy_global_config(config):
    repo_dir = get_repo_dir(config)
    global_dir = '{0}/config/ubuntu-18.04/global'.format(repo_dir)
    nginx_conf = '/etc/nginx/nginx.conf'
    uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
    uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'

    with cd(global_dir):
        sudo('cp nginx.conf {0}'.format(nginx_conf))
        set_permissions_file(nginx_conf, 'root', 'root', '644')

        sudo('cp uwsgi-app@.socket {0}'.format(uwsgi_socket))
        set_permissions_file(uwsgi_socket, 'root', 'root', '644')

        sudo('cp uwsgi-app@.service {0}'.format(uwsgi_service))
        set_permissions_file(uwsgi_service, 'root', 'root', '644')

    sudo('/etc/init.d/nginx restart')


def shutdown(config, branch=''):
    configuration = CONFIGURATIONS[config]
    if not branch:
        branch = configuration['branch']
    use_ssl = configuration['ssl']

    repo_dir = get_repo_dir(config)
    nginx_dir = '{0}/config/ubuntu-18.04/nginx/shutdown'.format(repo_dir)

    _update_source(repo_dir, branch)
    _reload_web(config, nginx_dir, use_ssl)
