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






class AuthTestCase(TestCase):
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

   

class UserDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.user_detail_url = reverse('user_detail', args=[self.user.id])
        
        # Log in the test user and get the token
        login_response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, content_type='application/json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.token = login_response.data['access']
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_get_user_detail(self):
        response = self.client.get(self.user_detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

    def test_get_user_detail_not_found(self):
        response = self.client.get(reverse('user_detail', args=[999]), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'No user found')

    def test_update_user_detail(self):
        data = {'email': 'updatedemail@example.com', 'username': 'updatedusername'}
        response = self.client.put(self.user_detail_url, data=json.dumps(data), content_type='application/json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updatedemail@example.com')
        self.assertEqual(self.user.username, 'updatedusername')

    def test_update_user_detail_not_found(self):
        data = {'email': 'updatedemail@example.com', 'username': 'updatedusername'}
        response = self.client.put(reverse('user_detail', args=[999]), data=json.dumps(data), content_type='application/json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'No user found')

    def test_delete_user(self):
        response = self.client.delete(self.user_detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_user_not_found(self):
        response = self.client.delete(reverse('user_detail', args=[999]), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'No user found')

    def test_unauthenticated_access(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.user_detail_url, data=json.dumps({'email': 'newemail@example.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        