"""
URL configuration for dcrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.home, name=''),
   path('register', views.register, name="register"),
   path('my-login', views.my_login, name="my-login"),
   path('user-logout', views.user_logout, name="user-logout"),
   ############## CRUD #######################
   # READ 
   path('dashboard', views.dashboard, name="dashboard"),

   #Create
   path('create-record', views.create_record, name="create-record"),

   #Update
   path('update-record/<int:pk>', views.update_record, name="update-record")
]
