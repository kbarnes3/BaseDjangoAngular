from importlib import import_module
from subprocess import check_output
from sys import argv

if len(argv) < 2:
    print('config required')
    exit(1)

config = argv[1]
django_settings = import_module('newdjangosite.settings_{0}'.format(config))
db_settings = django_settings.DATABASES['default']
db_name = db_settings['NAME']
db_user = db_settings['USER']
db_password = db_settings['PASSWORD']

database_exists_count = check_output([
    'psql',
    'postgres',
    '-tAc',
    "SELECT 1 FROM pg_catalog.pg_database WHERE datname='{0}'".format(db_name)])
if '1' in database_exists_count.decode('utf-8'):
    print('{0} already exists'.format(db_name))
else:
    print('Creating {0}'.format(db_name))
