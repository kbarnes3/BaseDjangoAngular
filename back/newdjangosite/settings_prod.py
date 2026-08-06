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

# Real outbound email over SMTP. Credentials come from the prod secrets env file.
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

ALLOWED_HOSTS = ['base.kbarnes3.com']

STATIC_ROOT = '/var/www/newdjangosite-prod/static'

# =============================================================================
# WARNING: PRODUCTION SIGNUPS ARE DISABLED
# =============================================================================
# This setting blocks all new account creation at the API level (signup
# endpoints return 403). It intentionally overrides the 'default' value from
# settings_base.py for the production deployment only.
#
# DO NOT change this value unless you have explicitly decided that public
# signups should be allowed in production. Flipping this back to 'default'
# (or 'notify') will immediately re-open account creation to anyone who can
# reach the production site.
#
# Valid values:
#   'default'  - normal signup behavior (PUBLIC SIGNUPS ENABLED)
#   'notify'   - signup works, ADMINS are emailed on each new account
#   'disabled' - signup blocked at the API level (current prod setting)
# =============================================================================
ACCOUNT_CREATION_MODE = 'disabled'
