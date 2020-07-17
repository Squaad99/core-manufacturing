from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from company.models import Company
from users.models import Profile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='username', email='email@email.com')
        user.set_password('password')
        user.save()
        self.client.login(username='username', password='password')
        self.company = Company(title='Company', currency='SEK', cost_per_work_hour='600')
        self.company.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.company = self.company
        user_profile.save()

    def test_user_profile_view(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
