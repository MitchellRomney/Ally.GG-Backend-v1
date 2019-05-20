from AllyGG.settings import *
import sentry_sdk
import dj_database_url

RIOT_API_KEY = os.environ.get('RIOT_API_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')


sentry_sdk.init(
    dsn="https://ee789799be9c4c3ab7411232f46b164c@sentry.io/1444367",
    integrations=[DjangoIntegration()],
    environment='API (Production)',
)

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = [
    'api.ally.gg'
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'https://www.ally.gg',
    'http://www.ally.gg',
    'www.ally.gg'
)

DEBUG = False

DEVELOPER_MODE = False

SECURE_SSL_REDIRECT = True

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

AWS_S3_REGION_NAME = 'us-east-2'

AWS_S3_ENDPOINT_URL = 'https://s3-us-east-2.amazonaws.com'

S3DIRECT_DESTINATIONS = {
    'profiles': {
        'key': 'uploads/profiles',
    },
    'projects': {
        'key': 'uploads/projects',
    },
    'services': {
        'key': 'uploads/services',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CELERY_BEAT_SCHEDULE = {
    'task_update_summoners': {
        'task': 'dashboard.tasks.task_update_summoners',
        'schedule': 3,
    },
    'task_update_version': {
        'task': 'dashboard.tasks.task_update_version',
        'schedule': crontab(minute='*/1'),
    },
    'task_update_stats': {
        'task': 'dashboard.tasks.task_update_stats',
        'schedule': 30,
    },
}