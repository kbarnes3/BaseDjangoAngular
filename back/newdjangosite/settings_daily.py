from .settings_base import *  #pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdjangosite_daily',
        'USER': 'newdjangosite_daily_user',
        'PASSWORD': 'passwordgoeshere',
        'HOST': 'localhost',
        'PORT': '',
    }
}


EMAIL_SUBJECT_PREFIX = '[newdjangosite-daily] '

ALLOWED_HOSTS = ['daily.yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-daily/static'
