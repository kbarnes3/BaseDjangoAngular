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

ALLOWED_HOSTS = ['yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-prod/static'
