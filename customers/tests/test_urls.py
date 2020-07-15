from django.test import SimpleTestCase
from django.urls import reverse, resolve

from customers.views import Overview, Create


class TestUrls(SimpleTestCase):

    def test_customer_overview_is_resolved(self):
        url = reverse('customer-overview')
        self.assertEqual(resolve(url).func.view_class, Overview)

    def test_customer_create_is_resolved(self):
        url = reverse('customer-create')
        self.assertEqual(resolve(url).func.view_class, Create)
