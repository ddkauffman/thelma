import os
import json
from unipath import Path
import requests

from celery.decorators import task

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).ancestor(2)
MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("static")


def get_env_variable(var_name):

    try:
        return os.environ[var_name]
    except Exception as err:
        print(err.args[0])
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('THELMA_SECRET_KEY')

SEMANTIC_VERSION = {
    'major': 1,
    'minor': 1,
    'patch': 0,
    'release': '',
}



# JETA API Configuration

TELEMETRY_API_HOST = get_env_variable('TELEMETRY_API_HOST')
TELEMETRY_API_PORT = get_env_variable('TELEMETRY_API_PORT')

API_USER = 'svc_jska'
API_PASSWORD = 'svc_jska'

HTTP_PROTOCOL = get_env_variable('HTTP_PROTOCOL')

API_URL = f'{HTTP_PROTOCOL}://{TELEMETRY_API_HOST}{TELEMETRY_API_PORT}/api/token/'

# Celery


@task
def get_new_token():

    API_URL = f'{HTTP_PROTOCOL}://{TELEMETRY_API_HOST}{TELEMETRY_API_PORT}/api/token/'

    API_TOKENS = requests.post(API_URL, json={
            'username': API_USER,
            'password': API_PASSWORD
        }
    ).json()

    os.environ['API_ACCESS_TOKEN'] = API_TOKENS['access']
    # os.environ['API_REFRESH_TOKEN'] = API_TOKENS['refresh']
    print('New Access Token Set')


BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_BEAT_SCHEDULE = {
  'refresh_token': {
        'task': 'get_new_token',
        'schedule': 300.0,
        'args': ()
    },
}

try:
    print(f'Setting init token ... ')
    API_TOKENS = requests.post(API_URL, json={
            'username': API_USER,
            'password': API_PASSWORD
        }
    ).json()

    os.environ['API_ACCESS_TOKEN'] = API_TOKENS['access']
    # os.environ['API_REFRESH_TOKEN'] = API_TOKENS['refresh']
    print(f'Token set ... ')
except Exception as err:
    import datetime
    print(f'Could not init API Token: {err.args[0]} {datetime.datetime.now().isoformat()}')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost', '*.stsci.edu']
FORCE_SCRIPT_NAME = ""


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'thelma.core',
    'thelma.fetch',
    'thelma.ingest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'thelma.core.middleware.auth.RHEL7CustomHeaderMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = (
    BASE_DIR.parent.child("assets"),
    # "thelma/assets",
    os.path.join(BASE_DIR.parent.child("assets"), 'vendor/node_modules/lib/'),
)
