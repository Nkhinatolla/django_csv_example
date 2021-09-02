web: gunicorn csv_example.wsgi
worker: celery -A csv_example.celery worker -l INFO -Q csv_example -c 1