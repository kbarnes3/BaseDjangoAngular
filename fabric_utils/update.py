from colorama import Fore, init
from fabric import Task
from fabric.transfer import Transfer
from plush.fabric_commands.permissions import ensure_directory


init(autoreset=True)


@Task
def compile_requirements(conn, fresh=False, update=False):
    print(Fore.GREEN + 'Compiling Python requirements')
    remote_user = conn.run('whoami').stdout.strip()
    ensure_directory(conn, '/tmp/pip-tools', remote_user)
    conn.sudo('rm -rf /tmp/pip-tools/*')

    transfer = Transfer(conn)
    transfer.put('requirements.in', '/tmp/pip-tools/requirements.in')

    if not fresh:
        transfer.put('ubuntu64-py310-requirements.txt', '/tmp/pip-tools/ubuntu64-py310-requirements.txt')

    print(Fore.GREEN + 'Setting up virtualenv')
    with conn.cd('/tmp/pip-tools/'):
        conn.run('python3 -m venv venv')

        print(Fore.GREEN + 'Updating pip')
        conn.run('venv/bin/python -m pip install --upgrade pip')

        print(Fore.GREEN + 'Updating pip-tools')
        conn.run('venv/bin/python -m pip install --upgrade pip-tools')

        print(Fore.GREEN + 'Compiling requirements')
        conn.run('venv/bin/pip-compile --output-file=ubuntu64-py310-requirements.txt requirements.in')

    transfer.get('/tmp/pip-tools/ubuntu64-py310-requirements.txt', 'ubuntu64-py310-requirements.txt')
    print(Fore.GREEN + 'Updated ubuntu64-py310-requirements.txt')
    print(Fore.GREEN + 'Removing temp files')
    conn.sudo('rm -rf /tmp/pip-tools')
