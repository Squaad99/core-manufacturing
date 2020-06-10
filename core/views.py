import os
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from users.models import Company, Profile


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

        profile = Profile.objects.get(user=self.request.user.id)
        context['user_profile'] = profile

        context['company_users'] = Profile.objects.filter(company=profile.company)

        return context
