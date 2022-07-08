import environ
from .settings_base import *    #pylint: disable=unused-wildcard-import, wildcard-import

ENV = environ.Env()
environ.Env.read_env('/var/www/python/newdjangosite-prod-secrets/prod/prod.env')

DEBUG = False

SECRET_KEY = ENV('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdjangosite_prod',
        'USER': 'newdjangosite_prod_user',
        'PASSWORD': ENV('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_SUBJECT_PREFIX = '[newdjangosite-prod] '

EMAIL_HOST = ENV('EMAIL_HOST')
EMAIL_PORT = ENV('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = ENV('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = ENV('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = ENV('EMAIL_USE_TLS', cast=bool, default=False)
EMAIL_USE_SSL = ENV('EMAIL_USE_SSL', cast=bool, default=False)

SERVER_EMAIL = 'newdjangosite-prod@yourdomain.tld'
DEFAULT_FROM_EMAIL = 'newdjangosite@yourdomain.tld'

ALLOWED_HOSTS = ['yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-prod/static'
