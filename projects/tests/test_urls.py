from django.test import SimpleTestCase
from django.urls import reverse, resolve

from projects.views import ProjectCreate, ProjectOverview


class TestUrls(SimpleTestCase):

    def test_project_overview_is_resolved(self):
        url = reverse('project-overview')
        self.assertEqual(resolve(url).func.view_class, ProjectOverview)

    def test_project_create_is_resolved(self):
        url = reverse('project-create')
        self.assertEqual(resolve(url).func.view_class, ProjectCreate)
