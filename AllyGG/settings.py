import os
import sentry_sdk
from celery.schedules import crontab
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://ee789799be9c4c3ab7411232f46b164c@sentry.io/1444367",
    integrations=[DjangoIntegration()]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'po4c8ty&7gr_z@6v65x#h_a(d*-2vbwg4t96s^_pzt&wi7m9^z'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'rest_framework',
    's3direct',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'AllyGG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'AllyGG.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'Apple123',
        'HOST': '',
        'PORT': '5432',
    }
}

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

CSRF_FAILURE_VIEW = 'dashboard.views.home'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'dashboard/static'),
)

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

RIOT_API_KEY = 'RGAPI-aaa5d257-9acd-4c6c-95df-552dff893091'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'dashboard.serializers.StandardResultsSetPagination',
    'PAGE_SIZE': 10
}

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Australia/Melbourne'
CELERY_BEAT_SCHEDULE = {
    'task_updateVersion': {
        'task': 'dashboard.tasks.task_update_version',
        'schedule': crontab(minute='*/5'),
    },
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000