from AllyGG.settings import *
import sentry_sdk
import dj_database_url

sentry_sdk.init(
    dsn="https://ee789799be9c4c3ab7411232f46b164c@sentry.io/1444367",
    integrations=[DjangoIntegration()],
    environment='Production',
)

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

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
        'schedule': 10,
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

def get_cache():
  import os
  try:
    servers = os.environ['MEMCACHIER_SERVERS']
    username = os.environ['MEMCACHIER_USERNAME']
    password = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,
        'LOCATION': servers,
        'OPTIONS': {
          'binary': True,
          'username': username,
          'password': password,
          'behaviors': {
            # Enable faster IO
            'no_block': True,
            'tcp_nodelay': True,
            # Keep connection alive
            'tcp_keepalive': True,
            # Timeout settings
            'connect_timeout': 2000, # ms
            'send_timeout': 750 * 1000, # us
            'receive_timeout': 750 * 1000, # us
            '_poll_timeout': 2000, # ms
            # Better failover
            'ketama': True,
            'remove_failed': 1,
            'retry_timeout': 2,
            'dead_timeout': 30,
          }
        }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()