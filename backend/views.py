import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
import logging

# Configure the logger
events_logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def event(request, name, location, starting_time, end_time ):
    try:
        # Return all events
        if request.method == 'GET':
            events = Event.objects.all()
            if events.exists():
                events_logger.debug('Events found')
                events_list = EventSerializer(events, many=True).data
                return Response({'events': events_list}, status=200)
            else:
                events_logger.debug('No events found')
                return Response({'message': 'No events found'}, status=404)
        
        # Create a new event
        if request.method == 'POST':
            data = request.data
            new_event = Event.objects.create(
                id=uuid.uuid4(),
                name= name,
                starting_time = starting_time,
                end_time = end_time,
                location = location
            )
            new_event.save()
            events_logger.debug('New event saved')
            return Response({'message': 'Event created successfully'}, status=201)
    except Exception as e:
        events_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)