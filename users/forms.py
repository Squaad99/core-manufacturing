from django import forms
from django.contrib.auth.admin import UserAdmin, admin
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from users.models import Company


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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('title',)
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

