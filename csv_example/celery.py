import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_example.settings')

app = Celery('csv_example')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
