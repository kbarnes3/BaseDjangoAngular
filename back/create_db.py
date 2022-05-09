from importlib import import_module
from subprocess import check_call, check_output
from sys import argv, exit as sys_exit

if len(argv) < 2:
    print('config required')
    sys_exit(1)

CONFIG = argv[1]
DJANGO_SETTINGS = import_module('newdjangosite.settings_{0}'.format(CONFIG))
DB_SETTINGS = DJANGO_SETTINGS.DATABASES['default']
DB_NAME = DB_SETTINGS['NAME']
DB_USER = DB_SETTINGS['USER']
DB_PASSWORD = DB_SETTINGS['PASSWORD']

DATABASE_EXISTS_COUNT = check_output([
    'psql',
    'postgres',
    '-tAc',
    "SELECT 1 FROM pg_catalog.pg_database WHERE datname='{0}'".format(DB_NAME)
])
if '1' in DATABASE_EXISTS_COUNT.decode('utf-8'):
    print('Database {0} already exists'.format(DB_NAME))
else:
    print('Creating database {0}'.format(DB_NAME))
    check_call([
        'createdb',
        '--encoding=UTF8',
        '--locale=en_US.UTF-8',
        '--owner=postgres',
        '--template=template0',
        DB_NAME
    ])
    print('{0} database created'.format(DB_NAME))

MATCHING_USER_COUNT = check_output([
    'psql',
    'postgres',
    '-tAc',
    "SELECT 1 FROM pg_roles WHERE rolname='{0}'".format(DB_USER)
])
if '1' in MATCHING_USER_COUNT.decode('utf-8'):
    print('User {0} already exists'.format(DB_USER))
else:
    print('Creating user {0}'.format(DB_USER))
    check_call([
        'createuser',
        '-s',
        DB_USER
    ])
    print('{0} user created'.format(DB_USER))

check_call([
    'psql',
    '-d',
    'postgres',
    '-c',
    "ALTER ROLE {0} WITH ENCRYPTED PASSWORD '{1}';".format(DB_USER, DB_PASSWORD)
])
print('Passsword updated for user {0}'.format(DB_USER))
