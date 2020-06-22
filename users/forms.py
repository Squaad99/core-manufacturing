from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


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
