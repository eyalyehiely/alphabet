import uuid,logging,json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth import authenticate,login as auth_login
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tasks import send_update_email
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status




events_logger = logging.getLogger('events')
users_logger =logging.getLogger('users')

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@ratelimit(key='user', rate='10/m', method=['GET', 'POST'], block=True)
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def events(request):
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
                name=data['name'],
                starting_time=data['starting_time'],
                end_time=data['end_time'],
                location=data['location'],
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            participants = []
            if 'participants' in data:
                for username in data['participants']:
                    try:
                        participant = User.objects.get(username=username)
                        new_event.participants.add(participant)
                        participants.append(participant.email)
                    except User.DoesNotExist:
                        events_logger.warning(f'User {username} does not exist')

            new_event.save()
            send_update_email.delay(new_event.id, participants, 'created')
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
            f'event_{event.id}',
            {
            'type': 'event_message',
            'message': f'Event "{event.name}" has been created.'
            })
            events_logger.debug('New event saved')
            return Response({'message': 'Event created successfully'}, status=201)
    except Exception as e:
        events_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)






@ratelimit(key='user', rate='10/m', method=['GET', 'PUT', 'DELETE'], block=True)
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def event(request, id):
    try:
        # Return specific event
        if request.method == 'GET':
            event = Event.objects.filter(id=id).first()
            if event:
                events_logger.debug('Event found')
                event_data = {
                    'id': event.id,
                    'name': event.name,
                    'starting_time': event.starting_time,
                    'end_time': event.end_time,
                    'location': event.location,
                    'participants': [user.username for user in event.participants.all()],
                    'created_at': event.created_at,
                    'updated_at': event.updated_at
                }
                return Response({'event': event_data}, status=200)
            else:
                events_logger.debug('No event found')
                return Response({'message': 'No event found'}, status=404)

        # Update event
        elif request.method == 'PUT':
            event = Event.objects.filter(id=id).first()
            if event:
                events_logger.debug(f'Event found: {event.name}, starting_time: {event.starting_time}, current_time: {timezone.now()}')
                if event.starting_time > timezone.now():
                    data = request.data
                    event.name = data.get('name', event.name)
                    event.starting_time = data.get('starting_time', event.starting_time)
                    event.end_time = data.get('end_time', event.end_time)
                    event.location = data.get('location', event.location)
                    event.updated_at = timezone.now()

                    participants = []
                    if 'participants' in data:
                        event.participants.clear()
                        for username in data['participants']:
                            try:
                                participant = User.objects.get(username=username)
                                event.participants.add(participant)
                                participants.append(participant.email)
                            except User.DoesNotExist:
                                events_logger.warning(f'User {username} does not exist')

                    event.save()
                    send_update_email.delay(event.id, participants, 'updated')
                    events_logger.debug('Event has been updated')

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f'event_{event.id}',
                        {
                            'type': 'event_message',
                            'message': f'Event "{event.name}" has been updated.'
                        }
                    )
                    return Response({'message': 'Event has been updated'}, status=200)
                else:
                    events_logger.debug(f'Event is in the past: {event.starting_time} <= {timezone.now()}')
                    return Response({'message': 'Event is in the past'}, status=404)
            else:
                events_logger.debug(f'No event found with id: {id}')
                return Response({'message': 'No event found'}, status=404)

        # Delete event
        elif request.method == 'DELETE':
            event = Event.objects.filter(id=id).first()
            if event:
                participants = [participant.email for participant in event.participants.all()]
                events_logger.debug('Event found')
                event.delete()
                send_update_email.delay(event.id, participants, 'deleted')
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'event_{event.id}',
                    {
                        'type': 'event_message',
                        'message': f'Event "{event.name}" has been deleted.'
                    }
                )
                events_logger.debug(f'Event {event.name} deleted')
                return Response({'message': f'Event {event.name} deleted'}, status=200)
            else:
                events_logger.debug('No events found')
                return Response({'message': 'No events found'}, status=404)
                
    except (ValueError, TypeError) as e:
        events_logger.debug(f'Invalid data received: {e}')
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        events_logger.error(f'Error occurred: {e}')
        return Response({'error': str(e)}, status=500)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='user', rate='10/m', method=['GET'], block=True)
def search_event(request, location):
    events = Event.objects.filter(location__icontains=location)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['POST', 'PUT', 'DELETE'])
@ratelimit(key='user', rate='10/m', method=['POST', 'PUT', 'DELETE'], block=True)
@permission_classes([IsAuthenticated])
def batch_events(request):
    try:
        data = request.data
        
        if request.method == 'POST':
            # Batch create events
            events = []
            for event_data in data:
                new_event = Event(
                    id=uuid.uuid4(),
                    name=event_data['name'],
                    starting_time=event_data['starting_time'],
                    end_time=event_data['end_time'],
                    location=event_data['location'],
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                participants = []
                if 'participants' in event_data:
                    for username in event_data['participants']:
                        try:
                            participant = User.objects.get(username=username)
                            new_event.participants.add(participant)
                            participants.append(participant.email)
                        except User.DoesNotExist:
                            events_logger.warning(f'User {username} does not exist')
                new_event.save()
                events.append(new_event)
                send_update_email.delay(new_event.id, participants, 'created')
                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'event_{new_event.id}',
                    {
                        'type': 'event_message',
                        'message': f'Event "{new_event.name}" has been created.'
                    }
                )
            events_logger.debug('Batch events created')
            return Response({'message': 'Batch events created successfully'}, status=201)

        elif request.method == 'PUT':
            # Batch update events
            for event_data in data:
                event = Event.objects.filter(id=event_data['id']).first()
                if event:
                    events_logger.debug(f'Event found: {event.name}, starting_time: {event.starting_time}, current_time: {timezone.now()}')
                    if event.starting_time > timezone.now():
                        event.name = event_data.get('name', event.name)
                        event.starting_time = event_data.get('starting_time', event.starting_time)
                        event.end_time = event_data.get('end_time', event.end_time)
                        event.location = event_data.get('location', event.location)
                        event.updated_at = timezone.now()

                        participants = []
                        if 'participants' in event_data:
                            event.participants.clear()
                            for username in event_data['participants']:
                                try:
                                    participant = User.objects.get(username=username)
                                    event.participants.add(participant)
                                    participants.append(participant.email)
                                except User.DoesNotExist:
                                    events_logger.warning(f'User {username} does not exist')

                        event.save()
                        send_update_email.delay(event.id, participants, 'updated')
                        events_logger.debug('Event has been updated')

                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(
                            f'event_{event.id}',
                            {
                                'type': 'event_message',
                                'message': f'Event "{event.name}" has been updated.'
                            }
                        )
                    else:
                        events_logger.debug(f'Event is in the past: {event.starting_time} <= {timezone.now()}')
            return Response({'message': 'Batch events updated successfully'}, status=200)

        elif request.method == 'DELETE':
            # Batch delete events
            for event_id in data:
                event = Event.objects.filter(id=event_id).first()
                if event:
                    participants = [participant.email for participant in event.participants.all()]
                    events_logger.debug('Event found')
                    event.delete()
                    send_update_email.delay(event.id, participants, 'deleted')
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f'event_{event.id}',
                        {
                            'type': 'event_message',
                            'message': f'Event "{event.name}" has been deleted.'
                        }
                    )
                    events_logger.debug(f'Event {event.name} deleted')
            return Response({'message': 'Batch events deleted successfully'}, status=200)
                
    except (ValueError, TypeError) as e:
        events_logger.debug(f'Invalid data received: {e}')
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        events_logger.error(f'Error occurred: {e}')
        return Response({'error': str(e)}, status=500)
# --------------------------------------------------users----------------------------------------------------------------------------------------------------
@csrf_exempt
@api_view(['POST'])
def signin(request):
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        users_logger.debug(f'Attempting login for username: {username}')

        if not User.objects.filter(username=username).exists():
            users_logger.debug('No user found')
            return Response({'status': 'error', 'message': 'Invalid Username'}, status=400)


        # Authenticate user
        user = authenticate(request,username=username, password=password)
        if user is not None:
            auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            refresh['first_name'] = user.first_name
            access = refresh.access_token
            users_logger.debug(f'{username} logged in')
            return Response({
                'status': 200,
                'refresh': str(refresh),
                'access':str(access)
            },status=200)
        else:
            users_logger.debug('Error logging in: Invalid username or password')
            return Response({'status': 'error', 'message': 'Invalid username or password'}, status=401)




@csrf_exempt
@api_view(['POST'])
def signup(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return Response({'error': 'Email, password, and username are required'}, status=400)

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)  
        user.save()

        users_logger.debug(f'user {user.username} created')
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        access = refresh.access_token
        users_logger.debug(f'{user.username} logged in')
        return Response({
            'status': 200,
            'refresh': str(refresh),
            'access': str(access)
        }, status=200)

    users_logger.debug('User not created')
    return Response(serializer.errors, status=400)





        

@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    try:
        # Retrieve specific user by ID
        if request.method == 'GET':
            user = User.objects.filter(id=user_id).first()
            if user:
                users_logger.debug('User found')
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.date_joined,  # Use date_joined for created_at
                    'updated_at': user.last_login  # Use last_login for updated_at
                }
                return Response({'user': user_data}, status=200)
            else:
                users_logger.debug('No user found')
                return Response({'message': 'No user found'}, status=404)
        
        # Update specific user by ID
        elif request.method == 'PUT':
            data = request.data
            user = User.objects.filter(id=user_id).first()
            if user:
                user.email = data.get('email', user.email)
                user.username = data.get('username', user.username)
                user.save()
                users_logger.debug('User updated')
                return Response({'message': 'User updated successfully'}, status=200)
            else:
                users_logger.debug('No user found')
                return Response({'message': 'No user found'}, status=404)
        
        # Delete specific user by ID
        elif request.method == 'DELETE':
            user = User.objects.filter(id=user_id).first()
            if user:
                user.delete()
                users_logger.debug('User deleted')
                return Response({'message': 'User deleted successfully'}, status=200)
            else:
                users_logger.debug('No user found')
                return Response({'message': 'No user found'}, status=404)

    except Exception as e:
        users_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)


