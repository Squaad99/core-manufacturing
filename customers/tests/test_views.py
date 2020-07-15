from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from company.models import Company
from customers.models import Customer
from users.models import Profile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='username')
        user.set_password('password')
        user.save()
        self.client.login(username='username', password='password')
        self.company = Company(title='Company', currency='SEK', cost_per_work_hour='600')
        self.company.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.company = self.company
        user_profile.save()


    def test_customer_create_POST(self):
        url = reverse('customer-create')

        self.client.post(url, {
            'title': 'customer',
            'comment': 'comment',
            'web_address': 'https://customer.com/',
            'company': self.company
        })

        customer = Customer.objects.get(pk=1)
        self.assertEqual(customer.title, 'customer')
        self.assertEqual(customer.company, self.company)
        self.assertEqual(customer.comment, 'comment')
