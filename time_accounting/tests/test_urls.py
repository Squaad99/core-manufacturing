from django.test import SimpleTestCase
from django.urls import reverse, resolve

from time_accounting.views import TimeReportCreate


class TestUrls(SimpleTestCase):

    def test_customer_overview_is_resolved(self):
        url = reverse('time-overview')
        self.assertEqual(resolve(url).func.view_class, TimeReportCreate)
