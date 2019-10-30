from .settings_base import *  #pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdjangosite_staging',
        'USER': 'newdjangosite_staging_user',
        'PASSWORD': 'passwordgoeshere',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_SUBJECT_PREFIX = '[newdjangosite-staging] '

ALLOWED_HOSTS = ['staging.yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-staging/static'
