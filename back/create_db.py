from importlib import import_module
from subprocess import check_call, check_output
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
    "SELECT 1 FROM pg_catalog.pg_database WHERE datname='{0}'".format(db_name)
])
if '1' in database_exists_count.decode('utf-8'):
    print('Database {0} already exists'.format(db_name))
else:
    print('Creating database {0}'.format(db_name))
    check_call([
        'createdb',
        '--encoding=UTF8',
        '--locale=en_US.UTF-8',
        '--owner=postgres',
        '--template=template0',
        db_name
    ])
    print('{0} database created'.format(db_name))

matching_user_count = check_output([
    'psql',
    'postgres',
    '-tAc',
    "SELECT 1 FROM pg_roles WHERE rolname='{0}'".format(db_user)
])
if '1' in matching_user_count.decode('utf-8'):
    print('User {0} already exists'.format(db_user))
else:
    print('Creating user {0}'.format(db_user))
    check_call([
        'createuser',
        '-s',
        db_user
    ])
    print('{0} user created'.format(db_user))

check_call([
    'psql',
    '-d',
    'postgres',
    '-c',
    "ALTER ROLE {0} WITH ENCRYPTED PASSWORD '{1}';".format(db_user, db_password)
])
print('Passsword updated for user {0}'.format(db_user))
