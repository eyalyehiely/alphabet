from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('events/', events, name='event_list'),
    path('event/<uuid:id>/', event, name='event_detail'),
    path('auth/signin/', signin, name='signin'),
    path('auth/signup/', signup, name='signup'),
    path('user/<int:user_id>/', user_detail, name='user_detail'), 
    path('search_event/<str:location>/', search_event, name='search_event'), 
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]