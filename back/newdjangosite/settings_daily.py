import environ
from .settings_base import *    #pylint: disable=unused-wildcard-import, wildcard-import

ENV = environ.Env()
environ.Env.read_env('/var/www/python/newdjangosite-daily-secrets/daily/daily.env')

DEBUG = False

SECRET_KEY = ENV('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newdjangosite_daily',
        'USER': 'newdjangosite_daily_user',
        'PASSWORD': ENV('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_SUBJECT_PREFIX = '[newdjangosite-daily] '

# Real outbound email over SMTP. Credentials come from the daily secrets env file.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': ENV('EMAIL_HOST'),
            'port': ENV.int('EMAIL_PORT'),
            'username': ENV('EMAIL_HOST_USER'),
            'password': ENV('EMAIL_HOST_PASSWORD'),
            'use_ssl': ENV.bool('EMAIL_USE_SSL'),
            # Bound the SMTP handshake so a slow relay can't tie up a uwsgi worker.
            'timeout': 10,
        },
    },
}

# Sender addresses. Must be verified with the SMTP provider or mail is rejected.
DEFAULT_FROM_EMAIL = ENV('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ALLOWED_HOSTS = ['daily.yourdomain.tld']

STATIC_ROOT = '/var/www/newdjangosite-daily/static'

# Public signups are enabled on this deployment. See settings_base.py for the
# other valid values of this setting.
ACCOUNT_CREATION_MODE = 'default'
