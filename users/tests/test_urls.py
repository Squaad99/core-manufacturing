from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import UserProfile, CustomLoginView


class TestUrls(SimpleTestCase):

    def test_user_profile_is_resolved(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, UserProfile)

    def test_login_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)
