import os
import sentry_sdk
import environ
from datetime import timedelta
from celery.schedules import crontab
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
RIOT_API_KEY = env('RIOT_API_KEY')

sentry_sdk.init(
    dsn="https://ee789799be9c4c3ab7411232f46b164c@sentry.io/1444367",
    integrations=[DjangoIntegration()],
    environment='API (Local)',
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'dashboard',
    'corsheaders',
    's3direct',
    'dynamic_preferences',
    'graphene_django',
    'channels',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'AllyGG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, ''), ],
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_IGNORE_RESULT = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Australia/Melbourne'
CELERY_BEAT_SCHEDULE = {
    'task_update_stats': {
        'task': 'dashboard.tasks.task_update_stats',
        'schedule': crontab(minute='*/5'),
    },
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

DYNAMIC_PREFERENCES = {

    'MANAGER_ATTRIBUTE': 'preferences',

    'REGISTRY_MODULE': 'dynamic_preferences_registry',

    'ADMIN_ENABLE_CHANGELIST_FORM': False,

    'SECTION_KEY_SEPARATOR': '__',

    'ENABLE_CACHE': False,

    'VALIDATE_NAMES': True,
}

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'localhost:8080'
)

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'httpOnly',
    'origin',
    'secure',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

GRAPHENE = {
    'SCHEMA': 'AllyGG.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=7),
}

# Channels
ASGI_APPLICATION = 'AllyGG.routing.application'

# Channels settings
CHANNEL_LAYERS = {
   "default": {
       "BACKEND": "channels_redis.core.RedisChannelLayer",
       "CONFIG": {
           "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
       },
   },
}

if DEBUG:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'testing@example.com'
