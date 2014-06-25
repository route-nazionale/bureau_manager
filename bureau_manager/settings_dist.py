# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#eh5w_tz$_e2)(hk0tm@qirunu=14m*5l%(9inlfxbgn+tf_p-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'bureau_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
