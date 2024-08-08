# events/tests.py
from django.test import TestCase, Client
from django.utils import timezone
from .models import Event
from datetime import datetime
import pytz,json
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


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
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        
        self.signin_url = reverse('signin')
        self.signup_url = reverse('signup')
        self.users_url = reverse('users_list')
        self.user_detail_url = reverse('user_detail', args=[self.user.id])

    def test_signin(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.signin_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_signup(self):
        data = {
            'username': 'signupuser',
            'email': 'signupuser@example.com',
            'password': 'signuppassword'
        }
        response = self.client.post(self.signup_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username='signupuser').exists())

    def test_get_users(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)

    def test_create_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(self.users_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_get_user_detail(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_update_user_detail(self):
        data = {'email': 'updatedemail@example.com'}
        response = self.client.put(self.user_detail_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updatedemail@example.com')

    def test_delete_user(self):
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())