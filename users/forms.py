from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserChangeForm
from django.contrib.auth.models import User


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Användarnamn',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password = forms.CharField(
        label='Lösenord',
        strip=False,
        widget=forms.PasswordInput
    )


class UserForm(UserChangeForm):
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
