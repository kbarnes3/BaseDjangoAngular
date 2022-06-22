from .settings_base import *  #pylint: disable=unused-wildcard-import, wildcard-import

# Settings for running a local development server using runserver

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'newdjangosite.db',
    }
}

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
