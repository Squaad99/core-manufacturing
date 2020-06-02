from django import forms
from django.contrib.auth.admin import UserAdmin, admin
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile


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


# class UserCreateForm(UserCreationForm):
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'password')
#
#
# class UserAdmin(UserAdmin):
#     add_form = UserCreateForm
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', 'company'),
#         }),
#     )
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('company')
