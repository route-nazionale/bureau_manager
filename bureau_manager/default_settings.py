"""
Django settings for bureau_manager project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, locale
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#eh5w_tz$_e2)(hk0tm@qirunu=14m*5l%(9inlfxbgn+tf_p-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'base',
#    'badge',
    'edda',

    'suit',
    #'django_admin_bootstrapped.bootstrap3',
    #'django_admin_bootstrapped',
    'django.contrib.admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bureau_manager.urls'

WSGI_APPLICATION = 'bureau_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# useful for strftime
locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')

YOUNG_AGE = 22

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/debug.log',
        },
        'rabbitfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/rabbitmq_send.log',
        },
        'stdout' : {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rabbit' : {
            'handlers': ['rabbitfile'],
            'level' : 'DEBUG',
            'propagate': False
        }
    },
}

MAX_USABLE_CODICE_CENSIMENTO = 2999
SUIT_CONFIG = {
    'ADMIN_NAME' : 'RN2014 - Segreteria',
    'LIST_PER_PAGE' : 100,
    'SEARCH_URL' : '',
    'MENU' : (
        {'app': 'edda', 'label': 'Gestione', },
    ),
    
}

RABBITMQ_ENABLE = False
RABBITMQ = {
    'host' : 'localhost',
}

REST_URL_GET_CU_GROUPS = "https://172.16.10.141/users/%(cu)s/groups"

SECRET_IV = ''
SECURE_KEY = '' 

