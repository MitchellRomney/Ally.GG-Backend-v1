release: python manage.py migrate
web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program daphne AllyGG.asgi:application --port $PORT --bind 0.0.0.0 -v2
celeryworker: celery -A AllyGG worker -l info --autoscale=6,3
celerybeatworker: celery -A AllyGG beat