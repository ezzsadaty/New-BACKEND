from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    location_list, camera_list, person_list, community_list, users_in_community_list, person_detail, camera_history_list, security_personnel_list, admin_list,
    add_camera_history, add_security_personnel, add_admin, create_community,
    add_user_to_community, add_person,users_in_community_by_id,remove_user_from_community,
)

urlpatterns = [
    path('locations/', location_list, name='location-list'),
    path('cameras/', camera_list, name='camera-list'),
    path('persons/', person_list, name='person-list'),
    path('Signup/', add_person, name='add-person'),
    path('persons/<int:pk>/', person_detail, name='person-detail'),
    path('communities/', community_list, name='community-list'),
    path('communities/create/', create_community, name='create-community'),
    path('users-in-community/', users_in_community_list,
         name='users-in-community-list'),
    path('add-user-to-community/', add_user_to_community,
         name='add-user-to-community'),
    path('remove_user_from_community/', remove_user_from_community, name='remove_user_from_community'),

    path('users-in-community/<int:community_id>/', users_in_community_by_id, name='users_in_community_by_id'),
    path('camera-history/', camera_history_list, name='camera-history-list'),
    path('security-personnels/', security_personnel_list,
         name='security-personnel-list'),
    path('admins/', admin_list, name='admin-list'),
    path('camera-history/add/', add_camera_history, name='add_camera_history'),
    path('security-personnel/add/', add_security_personnel,
         name='add_security_personnel'),
    path('admin/add/', add_admin, name='add_admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
