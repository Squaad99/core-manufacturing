from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from company.models import Company, ProjectState
from customers.models import Customer
from projects.models import Project
from users.models import Profile


class TestProjectViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='username')
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='username', password='password')
        self.company_1 = Company.objects.create(title='Company1', currency='SEK', cost_per_work_hour='600')
        self.company_2 = Company.objects.create(title='Company2', currency='SEK', cost_per_work_hour='600')
        user_profile = Profile.objects.get(user=self.user)
        user_profile.company = self.company_1
        user_profile.save()
        self.customer = Customer.objects.create(title="Customer 1", comment="Comment", created_by=self.user,
                                                company=self.company_1)
        self.customer_2 = Customer.objects.create(title="OtherCompanyCustomer", comment="Comment", created_by=self.user,
                                                  company=self.company_2)
        self.project_state = ProjectState.objects.create(title="State 1", index_position=1, display_table=True,
                                                         company=self.company_1)
        self.project_state_2 = ProjectState.objects.create(title="OtherCompanyState", index_position=1,
                                                           display_table=True, company=self.company_2)

    def test_project_create_POST(self):
        url = reverse('project-create')
        get_response = self.client.get(url)
        form_string = str(get_response.context['form']) + ""
        self.assertIn("Customer 1", form_string)
        self.assertNotIn('OtherCompanyCustomer', form_string)
        self.assertIn("State 1", form_string)
        self.assertNotIn('OtherCompanyState', form_string)

        self.client.post(url, {
            'title': "title",
            'comment': 'comment',
            'state': self.project_state.id,
            'customer': self.customer.id
        })

        project = Project.objects.get(pk=1)
        self.assertEqual(project.title, 'title')
        self.assertEqual(self.project_state.id, project.state.id)
        self.assertEqual(self.customer.id, project.customer.id)

    def test_project_update_POST(self):
        url = reverse('project-create')
        self.client.post(url, {
            'title': "beforeUpdate",
            'comment': 'commentBeforeUpdate',
            'state': self.project_state.id,
            'customer': self.customer.id
        })

        url = reverse('project-update', kwargs={'pk': 1})
        get_response = self.client.get(url)
        form_string = str(get_response.context['form'])
        self.assertIn("beforeUpdate", form_string)
        self.assertIn("commentBeforeUpdate", form_string)
        self.assertIn("Customer 1", form_string)
        self.assertNotIn('OtherCompanyCustomer', form_string)
        self.assertIn("State 1", form_string)
        self.assertNotIn('OtherCompanyState', form_string)

        self.client.post(url, {
            'title': "title",
            'comment': 'comment',
            'state': self.project_state.id,
            'customer': self.customer.id
        })

        project = Project.objects.get(pk=1)
        self.assertEqual(project.title, 'title')
        self.assertEqual(self.project_state.id, project.state.id)
        self.assertEqual(self.customer.id, project.customer.id)
