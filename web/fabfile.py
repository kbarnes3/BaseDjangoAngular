from fabric.api import env
from fabric_utils.deploy import deploy, deploy_global_config, shutdown
from fabric_utils.setup import add_authorized_key, setup_deployment, setup_server, setup_user

env.use_ssh_config = True  # This makes it easier to use key based authentication
