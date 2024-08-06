# signals.py
import logging
import smtplib
import ssl
import certifi
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Event

# Get an instance of a logger
logger = logging.getLogger('django')

@receiver(post_save, sender=Event)
def event_updated(sender, instance, created, **kwargs):
    if not created:  # Only trigger on updates, not on creation
        send_event_update_email(instance)

@receiver(pre_delete, sender=Event)
def event_deleted(sender, instance, **kwargs):
    send_event_delete_email(instance)

def send_event_update_email(event):
    subject = 'Event Updated'
    participants_list = ", ".join([p.username for p in event.participants.all()])
    body = (
        f'The event "{event.name}" has been updated.\n'
        f'New Details:\n'
        f'Location: {event.location}\n'
        f'Starting Time: {event.starting_time}\n'
        f'Participants: {participants_list}\n'
    )
    send_email_to_participants(event, subject, body)

def send_event_delete_email(event):
    subject = 'Event Cancelled'
    participants_list = ", ".join([p.username for p in event.participants.all()])
    body = (
        f'The event "{event.name}" has been cancelled.\n'
        f'Participants: {participants_list}\n'
    )
    send_email_to_participants(event, subject, body)

def send_email_to_participants(event, subject, body):
    context = ssl.create_default_context(cafile=certifi.where())
    from_email = settings.EMAIL_HOST_USER
    for participant in event.participants.all():
        if participant.email:
            try:
                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = participant.email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                message = msg.as_string()

                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.sendmail(from_email, participant.email, message)
                
                logger.info(f'Email sent to {participant.email} for event {event.name}')
            except Exception as e:
                logger.error(f'Failed to send email to {participant.email} for event {event.name}: {e}')