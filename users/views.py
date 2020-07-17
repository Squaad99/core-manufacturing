import os

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from users.forms import CustomAuthenticationForm, UserForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('users', 'profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    else:
        form = UserForm(instance=request.user)
        args = {'form': form}
        return render(request, os.path.join('users', 'user_form.html'), args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('profile'))
        else:
            return redirect(reverse('profile'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, os.path.join('users', 'password_form.html'), args)
