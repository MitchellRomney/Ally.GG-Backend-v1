release: python manage.py migrate
web: daphne AllyGG.asgi:application --port $PORT --bind 0.0.0.0 -v2
celeryworker: celery -A AllyGG worker -l info -B
socketworker: python manage.py runworker -v2
