"""core_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('materials/', include('materials.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

from users.views import CustomLoginView

urlpatterns = [
    path('', include('core.urls')),
    path('project/', include('projects.urls')),
    path('customer/', include('customers.urls')),
    path('product/', include('products.urls')),
    path('material/', include('materials.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('login/', CustomLoginView.as_view(template_name=os.path.join('users', 'login.html')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=os.path.join('users', 'logout.html')), name='logout'),
    path('admin/', admin.site.urls)
]
