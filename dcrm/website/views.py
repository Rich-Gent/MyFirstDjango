from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate 
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.http import HttpResponse

def home(request):
    return render(request, 'website/index.html')

#register a user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
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
                return redirect('dashboard')
    context = {'login_form':form}
    return render(request, 'website/my-login.html',context=context)

#logout user
def user_logout(request):

    auth.logout(request)
    return redirect("my-login")

#dashboard
@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'website/dashboard.html')