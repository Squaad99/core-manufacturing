from django.test import SimpleTestCase
from django.urls import reverse, resolve

from customers.views import Overview


class TestUrls(SimpleTestCase):

    def test_customer_overview_is_resolved(self):
        url = reverse('customer-overview')
        self.assertEqual(resolve(url).func.view_class, Overview)
