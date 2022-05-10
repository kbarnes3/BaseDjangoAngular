from importlib import import_module
from subprocess import check_call, check_output
from sys import argv, exit as sys_exit

if len(argv) < 2:
    print('config required')
    sys_exit(1)

CONFIG = argv[1]
DJANGO_SETTINGS = import_module(f'newdjangosite.settings_{CONFIG}')
DB_SETTINGS = DJANGO_SETTINGS.DATABASES['default']
DB_NAME = DB_SETTINGS['NAME']
DB_USER = DB_SETTINGS['USER']
DB_PASSWORD = DB_SETTINGS['PASSWORD']

DATABASE_EXISTS_COUNT = check_output([
    'psql',
    'postgres',
    '-tAc',
    f"SELECT 1 FROM pg_catalog.pg_database WHERE datname='{DB_NAME}'"
])
if '1' in DATABASE_EXISTS_COUNT.decode('utf-8'):
    print(f'Database {DB_NAME} already exists')
else:
    print(f'Creating database {DB_NAME}')
    check_call([
        'createdb',
        '--encoding=UTF8',
        '--locale=en_US.UTF-8',
        '--owner=postgres',
        '--template=template0',
        DB_NAME
    ])
    print(f'{DB_NAME} database created')

MATCHING_USER_COUNT = check_output([
    'psql',
    'postgres',
    '-tAc',
    f"SELECT 1 FROM pg_roles WHERE rolname='{DB_USER}'"
])
if '1' in MATCHING_USER_COUNT.decode('utf-8'):
    print(f'User {DB_USER} already exists')
else:
    print(f'Creating user {DB_USER}')
    check_call([
        'createuser',
        '-s',
        DB_USER
    ])
    print(f'{DB_USER} user created')

check_call([
    'psql',
    '-d',
    'postgres',
    '-c',
    f"ALTER ROLE {DB_USER} WITH ENCRYPTED PASSWORD '{DB_PASSWORD}';"
])
print(f'Passsword updated for user {DB_USER}')
