import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
import logging

# Configure the logger
events_logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def events(request, name, location, starting_time, end_time ):
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
    




@api_view(['GET','PUT','DELETE'])
def event(request, name, location, starting_time, end_time,id):
    try:
        # Return specific event
        if request.method == 'GET':
            event = Event.objects.filter(id=id).first()
            if event.exists():
                events_logger.debug('Event found')
                return Response({'event': event}, status=200)
            else:
                events_logger.debug('No events found')
                return Response({'message': 'No events found'}, status=404)
        
        # update event
        if request.method == 'PUT':
            try:
                event = Event.objects.filter(id=id).first()
                if event():
                    event.id = uuid.uuid4(),
                    event.name = name,
                    event.starting_time = starting_time,
                    event.end_time = end_time,
                    event.location = location
                    event.save()
                    events_logger.debug('Event has been updated')
                    return Response({'message': 'Event has been updated'}, status=200)
                else:
                    events_logger.debug('No event found')
                    return Response({'message': 'No event found'}, status=404)
                
            except (ValueError, TypeError) as e:
                events_logger.debug(f'Invalid data received: {e}')
                return Response({'error': str(e)}, status=400)

        
        if request.method == 'DELETE':
            event = Event.objects.filter(id=id).first()
            if event.exists():
                events_logger.debug('Event found')
                event.delete()
                return Response({'message': 'Event deleted'}, status=200)
            else:
                events_logger.debug('No events found')
                return Response({'message': 'No events found'}, status=404)
            
    except Exception as e:
        events_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)
