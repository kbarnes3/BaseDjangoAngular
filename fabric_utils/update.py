from colorama import Fore, init
from fabric import Task
from fabric.transfer import Transfer
from plush.fabric_commands.permissions import ensure_directory


init(autoreset=True)


@Task
def compile_requirements(conn, fresh=False, upgrade=False):
    print(Fore.GREEN + 'Compiling Python requirements')
    remote_user = conn.run('whoami').stdout.strip()

    staging_dir = '/tmp/pip-tools'

    ensure_directory(conn, staging_dir, remote_user)
    conn.sudo(f'rm -rf {staging_dir}/*')

    requirements_in = 'requirements.in'
    dev_requirements_in = 'dev-requirements.in'
    requirements_txt = 'ubuntu64-py310-requirements.txt'
    dev_requirements_txt = 'ubuntu64-py310-dev-requirements.txt'

    transfer = Transfer(conn)
    transfer.put(requirements_in, f'{staging_dir}/{requirements_in}')
    transfer.put(dev_requirements_in, f'{staging_dir}/{dev_requirements_in}')

    if not fresh:
        transfer.put(requirements_txt, f'{staging_dir}/{requirements_txt}')
        transfer.put(dev_requirements_txt, f'{staging_dir}/{dev_requirements_txt}')

    print(Fore.GREEN + 'Setting up virtualenv')
    with conn.cd(staging_dir):
        conn.run('python3 -m venv venv')

        print(Fore.GREEN + 'Updating pip')
        conn.run('venv/bin/python -m pip install pip==22.0.4')

        print(Fore.GREEN + 'Updating pip-tools')
        conn.run('venv/bin/python -m pip install --upgrade pip-tools')

        print(Fore.GREEN + 'Compiling requirements')
        upgrade_flag = ''
        if upgrade:
            upgrade_flag = '--upgrade'
        conn.run(f'venv/bin/pip-compile {upgrade_flag} --output-file={requirements_txt} ' +
                 f'{requirements_in}')

        print(Fore.GREEN + 'Compiling dev requirements')
        upgrade_flag = ''
        if upgrade:
            upgrade_flag = '--upgrade'
        conn.run(f'venv/bin/pip-compile {upgrade_flag} --output-file={dev_requirements_txt} ' +
                 f'{requirements_in} {dev_requirements_in}')

    transfer.get(f'{staging_dir}/{requirements_txt}', requirements_txt)
    print(Fore.GREEN + f'Updated {requirements_txt}')
    transfer.get(f'{staging_dir}/{dev_requirements_txt}', dev_requirements_txt)
    print(Fore.GREEN + f'Updated {dev_requirements_txt}')
    print(Fore.GREEN + 'Removing temp files')
    conn.sudo('rm -rf /tmp/pip-tools')
