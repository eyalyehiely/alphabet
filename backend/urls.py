from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('events/', events, name='event_list'),
    path('event/<uuid:id>/', event, name='event_detail'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('users/', users, name='event_list'),
    path('user/<uuid:id>/', user, name='user_detail'),   
]