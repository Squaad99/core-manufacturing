from django.test import SimpleTestCase
from django.urls import reverse, resolve

from company.views import EmployeeDelete, EmployeeUpdate, EmployeeCreate, CompanyUpdate, CompanyProfileView, \
    ProjectStateCreate, ProjectStateUpdate, ProjectStateDelete


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

    def test_project_state_create_is_resolved(self):
        url = reverse('company-project-state-create')
        self.assertEqual(resolve(url).func.view_class, ProjectStateCreate)

    def test_project_state_update_is_resolved(self):
        url = reverse('company-project-state-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProjectStateUpdate)

    def test_project_state_delete_is_resolved(self):
        url = reverse('company-project-state-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProjectStateDelete)
