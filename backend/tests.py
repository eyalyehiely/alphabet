# events/tests.py
from django.test import TestCase
from django.utils import timezone
from .models import Event
from datetime import datetime
import pytz

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