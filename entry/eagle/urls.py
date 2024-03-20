from django.urls import path
from .views import (
    location_list, camera_list, person_list, community_list, users_in_community_list
    , camera_history_list, security_personnel_list, admin_list
)

urlpatterns = [
    path('locations/', location_list, name='location-list'),
    path('cameras/', camera_list, name='camera-list'),
    path('persons/', person_list, name='person-list'),
    path('communities/', community_list, name='community-list'),
    path('users-in-community/', users_in_community_list, name='users-in-community-list'),
    #path('person-history/', person_history_list, name='person-history-list'),
    path('camera-history/', camera_history_list, name='camera-history-list'),
    path('security-personnels/', security_personnel_list, name='security-personnel-list'),
    path('admins/', admin_list, name='admin-list'),
]
