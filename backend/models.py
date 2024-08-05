import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    starting_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='participating_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_time <= self.starting_time:
            raise ValidationError('End time must be greater than start time.')

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super(Event, self).save(*args, **kwargs)