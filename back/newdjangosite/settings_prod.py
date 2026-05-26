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
