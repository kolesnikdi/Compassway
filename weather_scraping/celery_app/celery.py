from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_scraping.settings')

app = Celery('celery_app',
             broker=settings.CELERY_BROKER_URL, include=['celery_app.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.worker_send_task_events = True
app.autodiscover_tasks()
app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'


app.conf.update(result_backend='django-db', result_extended=True,)

if __name__ == '__main__':
    app.start()
