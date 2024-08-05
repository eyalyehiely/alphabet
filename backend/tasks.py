import logging
import smtplib
import ssl
import certifi
from celery import shared_task
from django.utils import timezone
from .models import Event
from datetime import timedelta
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get an instance of a logger
logger = logging.getLogger('celery')

@shared_task
def send_event_reminder():
    logger.debug('Task send_event_reminder started')
    now = timezone.now()
    reminder_time_start = now + timedelta(minutes=30)
    reminder_time_end = now + timedelta(minutes=31)  # Check for events starting within the next 30-31 minutes
    events = Event.objects.filter(starting_time__gte=reminder_time_start, starting_time__lt=reminder_time_end)
    
    if not events.exists():
        logger.debug('No upcoming events found for reminder')
        return

    context = ssl.create_default_context(cafile=certifi.where())
    
    for event in events:
        logger.debug(f'Processing event: {event.name}')
        for participant in event.participants.all():
            try:
                if not participant.email:
                    logger.warning(f'Participant {participant.username} has no email address')
                    continue

                from_email = settings.EMAIL_HOST_USER
                recipient_email = participant.email
                subject = 'Event Reminder'
                body = f'Reminder: Your event "{event.name}" is starting in 30 minutes.\n location: {event.location}\n participants: {event.participants.all()}\n'

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Convert the message to a string
                message = msg.as_string()

                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.sendmail(from_email, recipient_email, message)
                
                logger.debug(f'Reminder email sent to {participant.email} for event {event.name}')
            except Exception as e:
                logger.error(f'Failed to send reminder email to {participant.email} for event {event.name}: {e}')
    logger.debug('Task send_event_reminder finished')