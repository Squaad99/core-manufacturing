from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProjectForm():
    title = forms.TextInput(required=True)
    title = forms.Textarea(required=False)
