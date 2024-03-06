from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Location, Camera, Person, Community, UsersInCommunity, Person_History, Camera_History, SecurityPersonnel, Admin

def location_list(request):
    locations = Location.objects.all()
    data = [{'name': location.name} for location in locations]
    return JsonResponse(data, safe=False)

def camera_list(request):
    cameras = Camera.objects.all()
    data = [{'name': camera.name, 'location': camera.location.name} for camera in cameras]
    return JsonResponse(data, safe=False)

def person_list(request):
    persons = Person.objects.all()
    data = [{'first_name': person.first_name, 'last_name': person.last_name, 'birth_date': person.birth_date, 'created_at': person.created_at} for person in persons]
    return JsonResponse(data, safe=False)

def community_list(request):
    communities = Community.objects.all()
    data = [{'name': community.name, 'Community_ID': community.Community_ID} for community in communities]
    return JsonResponse(data, safe=False)

def users_in_community_list(request):
    users_in_community = UsersInCommunity.objects.all()
    data = [{'person': user.person.first_name, 'Community_ID': user.Community_ID.Community_ID, 'join_date': user.join_date} for user in users_in_community]
    return JsonResponse(data, safe=False)

def person_history_list(request):
    person_history = Person_History.objects.all()
    data = [{'person': history.person.first_name, 'location': history.location.name, 'camera': history.camera.name, 'checkIn_time': history.checkIn_time, 'checkOut_time': history.checkOut_time} for history in person_history]
    return JsonResponse(data, safe=False)

def camera_history_list(request):
    camera_history = Camera_History.objects.all()
    data = [{'person': history.person.first_name, 'camera': history.camera.name, 'checkIn_time': history.checkIn_time, 'checkOut_time': history.checkOut_time} for history in camera_history]
    return JsonResponse(data, safe=False)

def security_personnel_list(request):
    security_personnels = SecurityPersonnel.objects.all()
    data = [{'first_name': personnel.first_name, 'last_name': personnel.last_name, 'birth_date': personnel.birth_date, 'created_at': personnel.created_at} for personnel in security_personnels]
    return JsonResponse(data, safe=False)

def admin_list(request):
    admins = Admin.objects.all()
    data = [{'first_name': admin.first_name, 'last_name': admin.last_name, 'created_at': admin.created_at, 'birth_date': admin.birth_date} for admin in admins]
    return JsonResponse(data, safe=False)
