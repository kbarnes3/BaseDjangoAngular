from .settings_base import *    #pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdjangosite_prod',
        'USER': 'newdjangosite_prod_user',
        'PASSWORD': 'passwordgoeshere',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_SUBJECT_PREFIX = '[newdjangosite-prod] '

ALLOWED_HOSTS = ['yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-prod/static'
