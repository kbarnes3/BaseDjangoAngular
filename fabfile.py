from fabric_utils.deploy import deploy, deploy_global_config, shutdown
from fabric_utils.setup import add_authorized_key, disable_ssh_passwords, setup_deployment, setup_server, setup_user

__all__ = [
    'add_authorized_key',
    'deploy',
    'deploy_global_config',
    'disable_ssh_passwords',
    'setup_deployment',
    'setup_server',
    'setup_user',
    'shutdown',
]
