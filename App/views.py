import requests
import pytz
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from App.queries import fetch_districts
from New import WA_API_BASE_URL, WA_API_KEY, client, API_KEY, BASE_URL
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from App.reports import get_reports


turnover_range_list = [
    ('Below 1 Crore', [0, 10000000]),
    ('Between 1 to 5 Crores', [10000000, 50000000]),
    ('Between 5 to 10 Crores', [50000000, 100000000]),
    ('Between 10 to 25 Crores', [100000000, 250000000]),
    ('Between 25 to 50 Crores', [250000000, 500000000]),
    ('Between 50 to 100 Crores', [500000000, 1000000000]),
    ('Above 100 Crores', [1000000000, 10000000000])
]

language_list = [
    ('English', 'en'),
    ('Hindi', 'hi'),
    ('Bengali', 'bn')
]


def dashboard(request):
    reports = get_reports()
    if request.user.is_authenticated:
        return render(request, 'App/main_dashboard.html', {'reports': reports})

    else:
        return HttpResponseRedirect('/login/')


@login_required
def userlist(request):
    db = client['whatsapp']
    cursor = db.users.find().sort('created_on', -1)
    users = []
    categories = requests.get(BASE_URL+'/metadata/categories', headers={
        'Api-key': API_KEY}).json()["categories"]
    states = requests.get(BASE_URL+'/metadata/states', headers={
                          'Api-key': API_KEY}).json()["states"]
    for user in cursor:
        user['id'] = user['_id']
        user['work_categories'] = ', '.join(user['work_categories'])
        for turnover_range in turnover_range_list:
            if user['annual_turnover_range'] == turnover_range[1]:
                user['annual_turnover_range'] = turnover_range[0]
        users.append(user)
    return render(request, 'App/user_list.html', {'users': users,'response': categories,
                      'states': states,
                      'languages': language_list,
                      'turnover_list': [x[0] for x in turnover_range_list],})


@login_required
def notifications(request):
    return render(request, 'App/notifications.html')


@login_required
def settings(request):
    return render(request, 'App/settings.html')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'User Logged in Successfully!')
                    return HttpResponseRedirect('/')
                else:
                    messages.warning(
                        request, 'username or password not correct')
                    return redirect('/login/')

        else:
            fm = AuthenticationForm()
        return render(request, 'App/user_login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def new_user(request):
    categories = requests.get(BASE_URL+'/metadata/categories', headers={
        'Api-key': API_KEY}).json()["categories"]
    states = requests.get(BASE_URL+'/metadata/states', headers={
                          'Api-key': API_KEY}).json()["states"]
    return render(request, 'App/new_user.html',
                  {
                      'response': categories,
                      'states': states,
                      'languages': language_list,
                      'turnover_list': [x[0] for x in turnover_range_list],
                  })


def create_user(request):
    if request.method == "POST":
        form_data = request.POST
        # fileds needed in Array = work_category , preferred_states, preferred_districts
        required_field = ['work_categories',
                          'preferred_states', 'preferred_districts']
        # datatype = {type(required_field)}
        user_form_data = {}
        for key in form_data:
            if key == 'annual_turnover_range':
                user_form_data[key] = turnover_range_list[int(
                    form_data[key]) - 1][1]
                continue
            if key not in required_field:
                user_form_data[key] = form_data[key]
            else:
                user_form_data[key] = form_data.getlist(key)

        # Post the data to wa api
        api_url = WA_API_BASE_URL + '/users'
        res = requests.post(api_url, json=user_form_data,
                            headers={'Secret-Key': WA_API_KEY})
        if res.status_code == 201:
            messages.success(request, 'User Added Successfully!')
        elif res.status_code == 409:
            messages.warning(request, 'User Already Exists!')
        else:
            messages.warning(
                request, 'Something went wrong! Please try again!')

    return HttpResponseRedirect('/')


def update_user(request: HttpRequest, user_id: str):
    if request.method == "POST":
        form_data = request.POST
        # fileds needed in Array = work_category , preferred_states, preferred_districts
        required_field = ['work_categories',
                          'preferred_states', 'preferred_districts']
        # datatype = {type(required_field)}
        user_form_data = {}
        for key in form_data:
            if key == 'annual_turnover_range':
                user_form_data[key] = turnover_range_list[int(
                    form_data[key]) - 1][1]
                continue
            if key not in required_field:
                user_form_data[key] = form_data[key]
            else:
                user_form_data[key] = form_data.getlist(key)

        api_url = WA_API_BASE_URL + '/users'
        res = requests.patch(api_url, json=user_form_data,
                             headers={'Secret-Key': WA_API_KEY})
        if res.status_code == 200:
            messages.success(request, 'User Updated Successfully!')
        else:
            messages.warning(
                request, 'Something went wrong! Please try again!')

    categories = requests.get(BASE_URL+'/metadata/categories', headers={
        'Api-key': API_KEY}).json()["categories"]
    states = requests.get(BASE_URL+'/metadata/states', headers={
                          'Api-key': API_KEY}).json()["states"]
    user = client['whatsapp'].users.find_one({'_id': user_id})
    user['id'] = user['_id']
    for turnover_range in turnover_range_list:
        if user['annual_turnover_range'] == turnover_range[1]:
            user['annual_turnover_range'] = turnover_range[0]

    districts = fetch_districts(user['preferred_states'])
    return render(request, 'App/update_user.html',
                  {
                      'response': categories,
                      'states': states,
                      'districts': districts,
                      'languages': language_list,
                      'turnover_list': [x[0] for x in turnover_range_list],
                      'user': user
                  })


def get_districts(request: HttpRequest):
    if request.method == "POST":
        # data = request.POST.get("states")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        districts = fetch_districts(body['states'])
        return JsonResponse({'districts': districts})
