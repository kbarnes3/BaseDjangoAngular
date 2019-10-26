from .settings_base import *    #pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdjangosite_dev',
        'USER': 'newdjangosite_dev_user',
        'PASSWORD': 'passwordgoeshere',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_SUBJECT_PREFIX = '[newdjangosite-dev] '

ALLOWED_HOSTS = ['dev.yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-dev/static'
