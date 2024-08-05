from django.urls import path
from .views import *

urlpatterns = [
    path('events/', event, name='event_list'),
    path('events/<uuid:id>/', event, name='get_specific_event'),
   
]