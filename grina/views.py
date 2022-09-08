import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers

# Auth dependencies
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Redirect dependencies
from django.http import HttpResponseRedirect
from django.urls import reverse

# Hash 256
from hashlib import sha256

# API for courses & videotests(videocards)

def index(request):
    course_objects = serializers.serialize('json', Course.objects.all())
    course_objects_to_json = json.loads(course_objects)
    # New future json object
    courses_fixed_json = list()
    # Fixing Course objects
    for idx, item in enumerate(course_objects_to_json):
        # New stuff
        current_course = Course.objects.get(id=idx+1)
        course_datas = serializers.serialize('python', current_course.data.all())
        item['fields']['section'] = current_course.section
        item['fields']['data'] = course_datas
        # Fixing Data objects
        for idx2, data_item in enumerate(course_datas):
            # Hooking current Data object from Data object primary key  
            current_data = Data.objects.get(pk=json.loads(json.dumps(data_item))['pk'])
            # Removing superfluos from data object in json
            x = serializers.serialize('python', [current_data])
            item['fields']['data'][idx2] = x[0]['fields']
            # Adding id field to data json object
            item['fields']['data'][idx2]['id'] = x[0]['pk']
            # Hooking current SubCourses object from current Data object
            current_datas_subcourses =  serializers.serialize('python', current_data.sub_courses.all())
            item['fields']['data'][idx2]['sub_courses'] = current_datas_subcourses
            # Fixing SubCourse objects
            for idx3, subcourse_item in enumerate(current_datas_subcourses):
                current_subcourse = SubCourse.objects.get(pk=json.loads(json.dumps(subcourse_item))['pk'])
                y = serializers.serialize('python', [current_subcourse])
                item['fields']['data'][idx2]['sub_courses'][idx3] = y[0]['fields']

        # Saving all processed data to future json object
        courses_fixed_json.append(item['fields'])
 
    context = {
        'data': json.dumps(courses_fixed_json),
    }
    return render(request, 'grina/index.html', context)


# Get Video Object and craft a 
# course with given object's data

def get_craft(request, craft_id):

    # Get current Video Object
    video_objects = CraftStack.objects.get(id=craft_id).video_objects.all()

    # Init a void array to hold future data
    valid_json_video_objects = list()

    # Iterate over video_object items
    # and create cards
    for item in video_objects:
        item_to_json = serializers.serialize('python', [item])
        # Append to void array only 'field' JSON object
        valid_json_video_objects.append(item_to_json[0]['fields'])

    # At this point we have a list with all 
    # Video Objects in current course
    # Lets create a new one list to 
    # craft and append cards, videotests, parts etc...

    # craft array is a final result to show up
    craft = list()

    # Iterate over Video Objects we have
    for video_obj in valid_json_video_objects:
        # Craft cards
        card_json_object = {
            'type': 'card',
            'source': video_obj['source'],
            'eng_text': video_obj['eng_text'],
            'ru_text': video_obj['ru_text'],
            'tip': video_obj['tip'],
        }
        # append result of crafted cards
        craft.append(card_json_object)

    # Iterate over Video Objects again for tests
    for video_obj in valid_json_video_objects:
        # Handling server choice 1
        server_choice_1_obj = ServerChoice.objects.get(id=video_obj['server_choice_1'])
        # Fixint to JSON representation
        server_choice_1_json = serializers.serialize('python', [server_choice_1_obj])

        # Handling server choice 2
        server_choice_2_obj = ServerChoice.objects.get(id=video_obj['server_choice_2'])
        # Fixint to JSON representation
        server_choice_2_json = serializers.serialize('python', [server_choice_2_obj])

        # Handling server choice 3
        server_choice_3_obj = ServerChoice.objects.get(id=video_obj['server_choice_3'])
        # Fixint to JSON representation
        server_choice_3_json = serializers.serialize('python', [server_choice_3_obj])

        # Handling server choice 2
        server_choice_4_obj = ServerChoice.objects.get(id=video_obj['server_choice_4'])
        # Fixint to JSON representation
        server_choice_4_json = serializers.serialize('python', [server_choice_4_obj])

        # Setting up vtest data
        test_json_object = {
            'type': 'test',
            'source': video_obj['source'],
            'eng_text': video_obj['eng_text'],
            'ru_text': video_obj['ru_text'],
            'tip': video_obj['tip'],
            'server_choice_1': server_choice_1_json[0]['fields'],
            'server_choice_2': server_choice_2_json[0]['fields'],
            'server_choice_3': server_choice_3_json[0]['fields'],
            'server_choice_4': server_choice_4_json[0]['fields'],
        }  

        # Final setting Videotest data to craft
        craft.append(test_json_object)

    # Iterate one more time to craft sentence parts
    for video_obj in valid_json_video_objects:
        # Craft cards
        part_json_object = {
            'type': 'part',
            'source': video_obj['source'],
            'eng_text': video_obj['eng_text'],
            'ru_text': video_obj['ru_text'],
            'tip': video_obj['tip'],
        }

        # append result of crafted parts
        craft.append(part_json_object)

    context = {
        'data': json.dumps(craft),
    }

    return render(request, 'grina/craft.html', context)

'''

# Register, Login, Saving Progress


def register_new_user(request):
    email = request.GET['email']
    password = request.GET['password']

    user = User.objects.create_user(email, email, password)
    user.save()

    # Create user data as a storage
    input_ = email + password
    user_token = sha256(input_.encode('utf-8')).hexdigest()
    user_data = UserData(user_token=user_token, user_owner=user)
    user_data.save()

    # Giving user_token to user
    user_token_list = {
        'user_token': user_token
    }

    context = {
        'user_token_list': json.dumps(user_token_list),
    }

    return render(request, 'grina/get_user_token.html', context)

def login_user(request):
    email = request.GET['email']
    password = request.GET['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        user_data = UserData.objects.get(user_owner=user)
        user_data_json = serializers.serialize('python', [user_data])
        context = {
            'user_data': json.dumps(user_data_json),
        }
        return render(request, 'grina/get_user_data.html', context)
    else:
        return HttpResponse('Not OK')

# Google Register, Login
def register_new_user_google(request):
    google_email = request.GET['google_email']
    google_token = sha256(google_email.encode('utf-8')).hexdigest()

    user = User.objects.create_user(google_email, google_email, google_token)
    user.save()

    google_user_data = UserData(user_token=google_token, user_owner=user)
    google_user_data.save()

    # Giving user_token to user
    user_token_list = {
        'user_token': google_token
    }

    context = {
        'user_token_list': json.dumps(user_token_list),
    }

    return render(request, 'grina/get_user_token.html', context)

def login_user_google(request):
    google_email = request.GET['google_email']
    google_token = sha256(google_email.encode('utf-8')).hexdigest()

    google_user_data = UserData.objects.get(user_token=google_token)
    google_user_data_json = serializers.serialize('python', [google_user_data])

    context = {
        'user_data': json.dumps(google_user_data_json),
    }

    return render(request, 'grina/get_user_data.html', context)

'''