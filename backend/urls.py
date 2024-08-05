from django.urls import path
from .views import *

urlpatterns = [
    path('events/', events, name='event_list'),
    path('event/<uuid:id>/', event, name='event_detail'),
    # path('users/', UserListCreate.as_view(), name='user-list-create'),
    # path('users/<uuid:id>/', UserDetail.as_view(), name='user-detail'),
   
]