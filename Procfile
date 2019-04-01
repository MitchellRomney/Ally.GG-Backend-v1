release: python manage.py migrate
worker: celery -A AllyGG worker -l info -B
web: waitress-serve --port=$PORT AllyGG.wsgi:application
