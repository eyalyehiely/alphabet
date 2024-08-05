from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alphabet.settings')

app = Celery('alphabet')
from celery.schedules import crontab
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')




app.conf.beat_schedule = {
    'send-reminders-every-30-minutes': {
        'task': 'backend.tasks.send_event_reminder',
        'schedule': crontab(minute='*/30'),
    },
}