from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import pytz


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'starting_time', 'end_time', 'location', 'participants', 'created_at', 'updated_at']


    def get_participants(self, obj):
        return [participant.username for participant in obj.participants.all()]
    
    def get_created_at(self, obj):
        israel_tz = pytz.timezone('Asia/Jerusalem')
        created_at_israel = obj.created_at.astimezone(israel_tz)
        return created_at_israel.strftime('%d/%m/%Y %H:%M')

    def get_updated_at(self, obj):
        israel_tz = pytz.timezone('Asia/Jerusalem')
        updated_at_israel = obj.updated_at.astimezone(israel_tz)
        return updated_at_israel.strftime('%d/%m/%Y %H:%M')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        return token