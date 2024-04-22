from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth import authenticate 
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

from .models import Record
from datetime import date
import datetime
import requests
from django.conf import settings
import os

def home(request):
    return render(request, 'website/index.html')

#register a user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Successfully created!")
            return redirect('my-login')
    context = {'form': form}

    return render(request, 'website/register.html', context=context)
#login a user
def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have logged in successfully!")
                return redirect('dashboard')
    context = {'login_form':form}
    return render(request, 'website/my-login.html',context=context)

#logout user
def user_logout(request):

    auth.logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("my-login")

#dashboard
@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()
    context ={'records':my_records}
    return render(request, 'website/dashboard.html', context=context)

#Create a record
@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()
    if request.method =="POST":
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Record Successfully created!")
            return redirect("dashboard")
        
    context = {'create_form': form}
    return render(request, 'website/create-record.html', context=context)

#Update a record
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record Successfully updated!")
            return redirect("dashboard")
    context = {'update_form': form}
    return render(request, 'website/update-record.html', context=context)

@login_required(login_url='my-login')
def singular_record(request, pk):

    one_record = Record.objects.get(id=pk)
    context = {'record':one_record}
    return render(request, 'website/view-record.html',context=context)

#Delete a record
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Record Successfully Deleted!")
    return redirect("dashboard")

#request weather
def weatherRequest(request):
    api_path = os.path.join(settings.BASE_DIR,'API_KEY')
    API_KEY = open(api_path, "r").read()
    current_weather_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}/?key={}"
    # forecast_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{},{}/{}/{}?key={}"

    if request.method == "POST":
        try:
            city1 = request.POST['city1']
            weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url)

            context={
                "weather_data1": weather_data1,
                "daily_forecasts1": daily_forecasts1
            }
            return render(request, "website/weather.html",context)
        except:
            messages.error(request, "Please enter a valid city or town!")
            return render(request, "website/weather.html")
    else:
        return render(request, "website/weather.html")
    
def fetch_weather_and_forecast(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city,api_key)).json()
    #lat, lon = response["lattitude"],response["longitude"]
    #forecast_response = requests.get(forecast_url.format(lat,lon,))

    weather_data = {
        "city": city,
        "temperature": round((response["currentConditions"]["temp"]-32)*(5/9),2),
        "description": response["days"][0]["description"],
        "icon": response["days"][0]["icon"]
    }

    daily_forecasts = []
    for daily_data in response['days'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['datetimeEpoch']).strftime("%A"),
            "min_temp": round((daily_data['tempmin']-32)*(5/9),2),
            "max_temp": round((daily_data['tempmax']-32)*(5/9),2),
            "description": daily_data['description'],
            "icon": daily_data['icon']
        })
    
    return weather_data, daily_forecasts