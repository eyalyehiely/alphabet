from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Event
from datetime import timedelta

@shared_task
def send_event_reminder():
    now = timezone.now()
    reminder_time = now + timedelta(minutes=30)
    events = Event.objects.filter(starting_time__lte=reminder_time, starting_time__gt=now)
    
    for event in events:
        for participant in event.participants.all():
            send_mail(
                'Event Reminder',
                f'Reminder: Your event "{event.name}"  is starting in 30 minutes.',
                [participant.email],
                fail_silently=False,
            )