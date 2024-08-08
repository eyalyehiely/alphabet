# events/tests.py
from django.utils import timezone
from .models import Event
from datetime import datetime
import pytz
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

class EventTestCase(TestCase):
    def setUp(self):
        self.event1_start_time = datetime(2022, 1, 1, 10, 0, tzinfo=pytz.UTC)
        self.event1_end_time = datetime(2022, 1, 1, 12, 0, tzinfo=pytz.UTC)
        self.event2_start_time = datetime(2022, 1, 2, 11, 0, tzinfo=pytz.UTC)
        self.event2_end_time = datetime(2022, 1, 2, 13, 0, tzinfo=pytz.UTC)

        self.event1 = Event.objects.create(
            name='Event 1', 
            location='Location 1',
            starting_time=self.event1_start_time, 
            end_time=self.event1_end_time
        )
        self.event2 = Event.objects.create(
            name='Event 2', 
            location='Location 2',
            starting_time=self.event2_start_time, 
            end_time=self.event2_end_time
        )

    def test_event_create_event(self):
        event1 = Event.objects.get(name='Event 1')
        self.assertEqual(event1.name, 'Event 1')
        self.assertEqual(event1.location, 'Location 1')
        self.assertEqual(event1.starting_time, self.event1_start_time)
        self.assertEqual(event1.end_time, self.event1_end_time)

        event2 = Event.objects.get(name='Event 2')
        self.assertEqual(event2.name, 'Event 2')
        self.assertEqual(event2.location, 'Location 2')
        self.assertEqual(event2.starting_time, self.event2_start_time)
        self.assertEqual(event2.end_time, self.event2_end_time)

    def test_event_update_event(self):
        updated_name = 'Updated Event 1'
        updated_location = 'Updated Location 1'
        updated_start_time = datetime(2022, 1, 1, 11, 0, tzinfo=pytz.UTC)
        updated_end_time = datetime(2022, 1, 1, 13, 0, tzinfo=pytz.UTC)

        event1 = Event.objects.get(name='Event 1')
        event1.name = updated_name
        event1.location = updated_location
        event1.starting_time = updated_start_time
        event1.end_time = updated_end_time
        event1.save()

        updated_event1 = Event.objects.get(name='Updated Event 1')
        self.assertEqual(updated_event1.name, updated_name)
        self.assertEqual(updated_event1.location, updated_location)
        self.assertEqual(updated_event1.starting_time, updated_start_time)
        self.assertEqual(updated_event1.end_time, updated_end_time)

    def test_event_delete_event(self):
        event1 = Event.objects.get(name='Event 1')
        event1.delete()

        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(name='Event 1')






class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', email='testuser@example.com', password='admin')
        self.signin_url = reverse('signin')
        self.signup_url = reverse('signup')

    def test_signin_successful(self):
        data = {
            'username': 'admin',
            'password': 'admin'
        }
        response = self.client.post(self.signin_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_signin_invalid_username(self):
        data = {
            'username': 'invaliduser',
            'password': 'admin'
        }
        response = self.client.post(self.signin_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid Username')

    def test_signup_successful(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.signup_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_missing_fields(self):
        data = {
            'username': 'incompleteuser'
        }
        response = self.client.post(self.signup_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

   