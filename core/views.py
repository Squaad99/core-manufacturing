import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.
@login_required
def home(request):
    users = User.objects.all()
    users_names = []

    for user in users:
        users_names.append(user.first_name + " " + user.last_name)

    events = [
        'Projekt 1 uppdaterad',
        'Projekt 1 skapad',
        'Status 1 ändrad',
    ]

    context = {
        'users_names': users_names,
        'events': events
    }

    return render(request, os.path.join('core', 'home.html'), context)
