import uuid,logging,json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth import authenticate,login as auth_login
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# Configure the logger
events_logger = logging.getLogger('events')
users_logger =logging.getLogger('users')

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET', 'POST'])
def events(request, name, location, starting_time, end_time,participants ):
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
                participants = participants,
                starting_time = starting_time,
                end_time = end_time,
                location = location,
                created_at = timezone.now(),
                updated_at = timezone.now()
            )
            new_event.save()
            events_logger.debug('New event saved')
            return Response({'message': 'Event created successfully'}, status=201)
    except Exception as e:
        events_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)
    




@api_view(['GET','PUT','DELETE'])
def event(request, name, location, starting_time, end_time,id, participants):
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
                    'participants': [user.id for user in event.participants.all()],
                    'created_at': event.created_at,
                    'updated_at': event.updated_at
                }
                return Response({'event': event_data}, status=200)
            else:
                events_logger.debug('No event found')
                return Response({'message': 'No event found'}, status=404)
        
        # update event
        if request.method == 'PUT':
            try:
                event = Event.objects.filter(id=id).first()
                if event():
                    event.id = uuid.uuid4(),
                    event.name = name,
                    event.starting_time = starting_time,
                    event.end_time = end_time,
                    event.location = location,
                    event.participants = participants
                    if participants:
                        event.participants.clear()
                        for participant_id in participants:
                            event.participants.add(participant_id)
                    event.created_at = event.created_at
                    event.updated_at = timezone.now()
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
                events_logger.debug(f'Event {event.name} deleted')
                return Response({'message': f'Event {event.name} deleted'}, status=200)
            else:
                events_logger.debug('No events found')
                return Response({'message': 'No events found'}, status=404)
            
    except Exception as e:
        events_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)


# --------------------------------------------------users----------------------------------------------------------------------------------------------------
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


@api_view(['GET', 'POST'])
def users(request,email,password):
    try:
        # Return all users
        if request.method == 'GET':
            users = User.objects.all()
            if users.exists():
                users_logger.debug('users found')
                users_list = UserSerializer(users, many=True).data
                return Response({'users': users_list}, status=200)
            else:
                users_logger.debug('No users found')
                return Response({'message': 'No users found'}, status=404)
        
        # Create a new User
        if request.method == 'POST':
            new_user = User.objects.create(
                id = uuid.uuid4(),
                email = email,
                password = password,
                created_at = timezone.now(),
                updated_at = timezone.now()
            )
            new_user.save()
            users_logger.debug('New User saved')
            return Response({'message': 'User created successfully'}, status=201)
    except Exception as e:
        users_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)
    




@api_view(['GET','PUT','DELETE'])
def user(request,id, email, password):
    try:
        # Return specific user
        if request.method == 'GET':
            user = User.objects.filter(id=id).first()
            if user:
                users_logger.debug('user found')
                user_data = {
                    'id': user.id,
                    'email': user.email,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                }
                return Response({'user': user_data}, status=200)
            else:
                users_logger.debug('No user found')
                return Response({'message': 'No user found'}, status=404)
        
        # update user
        if request.method == 'PUT':
            try:
                user = user.objects.filter(id=id).first()
                if user():
                    user.id = uuid.uuid4(),
                    user.email = email,
                    user.password, = password,
                    user.created_at = user.created_at
                    user.updated_at = timezone.now()
                    user.save()
                    users_logger.debug('user has been updated')
                    return Response({'message': 'user has been updated'}, status=200)
                else:
                    users_logger.debug('No user found')
                    return Response({'message': 'No user found'}, status=404)
                
            except (ValueError, TypeError) as e:
                users_logger.debug(f'Invalid data received: {e}')
                return Response({'error': str(e)}, status=400)

        
        if request.method == 'DELETE':
            user = user.objects.filter(id=id).first()
            if user.exists():
                users_logger.debug(f'user {email} found')
                user.delete()
                users_logger.debug(f'user {email} deleted')
                return Response({'message': f'user {email} deleted'}, status=200)
            else:
                users_logger.debug('No users found')
                return Response({'message': 'No users found'}, status=404)
            
    except Exception as e:
        users_logger.error('Error occurred: %s', e)
        return Response({'error': str(e)}, status=500)