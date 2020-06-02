import os
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class Home(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('core', 'home.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        events = [
            'Projekt 1 uppdaterad 2',
            'Projekt 1 skapad',
            'Status 1 ändrad',
        ]
        context['events'] = events

        users = User.objects.all()
        users_names = []
        for user in users:
            users_names.append(user.first_name + " " + user.last_name)
        context['users_names'] = users_names

        current_user = User

        return context
