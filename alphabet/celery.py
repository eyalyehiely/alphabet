# your_project_name/celery.py

from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alphabet.settings')

app = Celery('alphabet')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-reminders-every-minute': {
        'task': 'backend.tasks.send_event_reminder',
        'schedule': crontab(minute='*'),  # Run every minute
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')