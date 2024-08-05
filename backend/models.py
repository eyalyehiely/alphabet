from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    id = models.UUIDField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 200)
    events = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    

class Event(models.Model):
    id = models.UUIDField()
    name = models.CharField(max_length = 200)
    starting_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
