import os
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.utils import get_most_recent_events
from users.models import Company, Profile


class Home(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('core', 'home.html')

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)

        context['events'] = get_most_recent_events(company)

        profile = Profile.objects.get(user=self.request.user.id)
        context['user_profile'] = profile

        context['company_users'] = Profile.objects.filter(company=profile.company)

        return context
