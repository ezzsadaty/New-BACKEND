from django.http import JsonResponse
from .models import Location, Camera, Person, Community, UsersInCommunity, Camera_History, SecurityPersonnel, Admin
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Camera_History, Person, Camera
import json
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password



def location_list(request):
    locations = Location.objects.all()
    data = [{'name': location.name} for location in locations]
    return JsonResponse(data, safe=False)


def camera_list(request):
    cameras = Camera.objects.all()
    data = [{'name': camera.name, 'location': camera.location.name}
            for camera in cameras]
    return JsonResponse(data, safe=False)


def person_list(request):
    persons = Person.objects.all()
    data = [{'id': person.pk,  'first_name': person.first_name, 'last_name': person.last_name,
            'birth_date': person.birth_date, 'created_at': person.created_at,
             'photo_url': person.photo.url if person.photo else None} for person in persons]
    return JsonResponse(data, safe=False)


def person_detail(request, pk):
    try:
        person = Person.objects.get(pk=pk)
        data = {
            'id': person.pk,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'birth_date': person.birth_date,
            'created_at': person.created_at,
            'email': person.email,
            'photo_url': person.photo.url if person.photo else None
        }
        return JsonResponse(data)
    except Person.DoesNotExist:
        return JsonResponse({'error': 'Person not found'}, status=404)


def community_list(request):
    communities = Community.objects.all()
    data = [{'name': community.name, 'Community_ID': community.Community_ID}
            for community in communities]
    return JsonResponse(data, safe=False)


@csrf_exempt
def create_community(request):
    if request.method == 'POST':
        # Decode JSON data from request body
        data = json.loads(request.body)
        # Extract data for creating a new community
        name = data.get('name')
        community_id = data.get('community_id')
        # Create a new community object
        community = Community(name=name, Community_ID=community_id)
        community.save()
        # Return a success response
        return JsonResponse({'message': 'Community created successfully'})
    else:
        # Return an error response for unsupported methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def users_in_community_list(request):
    users_in_community = UsersInCommunity.objects.all()
    data = [{'person': user.person.first_name, 'Community_ID': user.Community_ID.Community_ID,
             'join_date': user.join_date} for user in users_in_community]
    return JsonResponse(data, safe=False)


def users_in_community_by_id(request, community_id):
    # Query the database to retrieve users in the specified community
    users_in_community = UsersInCommunity.objects.filter(Community_ID=community_id)
    
    # Serialize the user data into JSON format
    data = [{'user_first': user.person.first_name,
             'photo_url': user.person.photo.url if user.person.photo else None, 
             'Community_ID': user.Community_ID.Community_ID,
             'join_date': user.join_date,
             'user_last': user.person.last_name,
             'user_id':user.person.pk} 
            for user in users_in_community]
    
    # Return the JSON response with the user data
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_user_to_community(request):
    if request.method == 'POST':
        # Decode JSON data from request body
        data = json.loads(request.body)

        # Extract data for creating a new UsersInCommunity object
        person_id = data.get('person_id')
        community_id = data.get('community_id')
        join_date = data.get('join_date')

        try:
            # Get person and community objects
            person = Person.objects.get(pk=person_id)
            community = Community.objects.get(pk=community_id)

            if UsersInCommunity.objects.filter(person=person, Community_ID=community).exists():
                return JsonResponse({'error': 'User already exists in the community'}, status=400)
            else:
                # Create a new UsersInCommunity object
                user_in_community = UsersInCommunity(person=person, Community_ID=community, join_date=join_date)
                user_in_community.save()
                # Return a success response
                return JsonResponse({'message': 'User added to community successfully'})
        except (Person.DoesNotExist, Community.DoesNotExist) as e:
            # Return an error response if person or community does not exist
            return JsonResponse({'error': 'Person or Community not found'}, status=404)
    else:
        # Return an error response for unsupported methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def remove_user_from_community(request):
    if request.method == 'POST':
        # Decode JSON data from request body
        data = json.loads(request.body)

        # Extract data for removing a user from the community
        person_id = data.get('person_id')
        community_id = data.get('community_id')

        try:
            # Get person and community objects
            person = Person.objects.get(pk=person_id)
            community = Community.objects.get(pk=community_id)

            # Check if the user exists in the community
            try:
                user_in_community = UsersInCommunity.objects.get(person=person, Community_ID=community)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'User does not exist in the community'}, status=400)

            # Remove the user from the community
            user_in_community.delete()

            # Return a success response
            return JsonResponse({'message': 'User removed from community successfully'})
        except (Person.DoesNotExist, Community.DoesNotExist) as e:
            # Return an error response if person or community does not exist
            return JsonResponse({'error': 'Person or Community not found'}, status=404)
    else:
        # Return an error response for unsupported methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def camera_history_list(request):
    camera_history = Camera_History.objects.all()
    data = [{'person': history.person.first_name, 'camera': history.camera.name,
             'checkIn_time': history.checkIn_time, 'checkOut_time': history.checkOut_time} for history in camera_history]
    return JsonResponse(data, safe=False)


def security_personnel_list(request):
    security_personnels = SecurityPersonnel.objects.all()
    data = [{'first_name': personnel.first_name, 'last_name': personnel.last_name,
             'birth_date': personnel.birth_date, 'created_at': personnel.created_at} for personnel in security_personnels]
    return JsonResponse(data, safe=False)


def admin_list(request):
    admins = Admin.objects.all()
    data = [{'first_name': admin.first_name, 'last_name': admin.last_name,
             'created_at': admin.created_at, 'birth_date': admin.birth_date} for admin in admins]
    return JsonResponse(data, safe=False)


@csrf_exempt  # Note: Be cautious with CSRF exemption in production
def add_camera_history(request):
    if request.method == 'POST':
        # Parse the JSON body of the request
        try:
            data = json.loads(request.body)
            person_name = data.get('name')
            person_id = data.get('id')
            checkIn_time = data.get('checkIn_time')
            checkOut_time = data.get('checkOut_time')
            camera_id = data.get('camera_id')
            print(data)
            print(checkIn_time)
            Cid = camera_id+1

            # Validate and fetch related instances
            person = Person.objects.filter(
                id=person_id, first_name=person_name).first()
            camera = Camera.objects.filter(id=Cid).first()

            if not person or not camera:
                return HttpResponseBadRequest("Invalid person ID/name or camera ID provided.")

            # Create the Camera_History record
            camera_history = Camera_History(
                person=person, camera=camera, checkIn_time=checkIn_time, checkOut_time=checkOut_time)
            camera_history.save()

            # Return success response
            return JsonResponse({'success': True, 'message': 'Camera history record added successfully.'})
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")
    else:
        # If not a POST request, return a 405 Method Not Allowed response
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def add_security_personnel(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data['first_name']
            last_name = data['last_name']
            birth_date = parse_date(data['birth_date'])

            security_personnel = SecurityPersonnel(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date
            )
            security_personnel.save()

            return JsonResponse({'success': True, 'message': 'Security personnel added successfully.'})
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def add_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            password = data['password']
            birth_date = parse_date(data['birth_date'])
            created_at = parse_date(data['created_at'])

            admin = Admin(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                created_at=created_at,
                username=username

            )
            admin.set_password(password)  # Set the hashed password
            admin.save()

            return JsonResponse({'success': True, 'message': 'Admin added successfully.'})
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def add_person(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Convert birth_date from string to date object
        birth_date_obj = birth_date
        if Person.objects.filter(username=username).exists() or Person.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Username or email already exists'}, status=400)
        # Assuming validation for each field is done here
        person = Person(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date_obj,
            email=email,
            photo=photo,
            username=username,
            password=password,
        )
        if password:
            person.password = make_password(password)

        # The save method in your Person model already handles the logic for the photo
        person.save()
        return JsonResponse({'status': 'success', 'person_id': person.id})

    return JsonResponse({'error': 'This method is not allowed'}, status=405)


@csrf_exempt
def login_person(request):
    if request.method == 'POST':
        # Decode JSON data from request body
        data = json.loads(request.body)

        # Extract username and password
        username = data.get('username')
        password = data.get('password')

        try:
            # Retrieve the person based on the username
            person = Person.objects.get(username=username)
        except Person.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

        # Check if the provided password matches the hashed password in the database
        if check_password(password, person.password):
            # Manually create session to log in person
            request.session['person_id'] = person.id
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        # Return an error response for unsupported methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username)
            if admin.check_password(password):
                # Authentication successful
                # Perform login logic here
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)