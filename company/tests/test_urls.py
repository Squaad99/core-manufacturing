from django.test import SimpleTestCase
from django.urls import reverse, resolve

from company.views import EmployeeDelete, EmployeeUpdate, EmployeeCreate, CompanyUpdate, CompanyProfileView


class TestUrls(SimpleTestCase):

    def test_company_profile_is_resolved(self):
        url = reverse('company-profile')
        self.assertEqual(resolve(url).func.view_class, CompanyProfileView)

    def test_company_profile_update_is_resolved(self):
        url = reverse('company-profile-update')
        self.assertEqual(resolve(url).func.view_class, CompanyUpdate)

    def test_employee_create_is_resolved(self):
        url = reverse('company-employee-create')
        self.assertEqual(resolve(url).func.view_class, EmployeeCreate)

    def test_employee_update_is_resolved(self):
        url = reverse('company-employee-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, EmployeeUpdate)

    def test_employee_delete_is_resolved(self):
        url = reverse('company-employee-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, EmployeeDelete)
