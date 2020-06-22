import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from projects.form import ProjectForm
from projects.models import Project, ProductForProject
from users.models import Profile, ProjectState


class ProjectOverview(LoginRequiredMixin, ListView):
    model = Project
    template_name = os.path.join('common', 'object_overview.html')
    context_object_name = 'projects'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Projekt'
        context['url_name'] = 'project'
        user_profile = Profile.objects.get(user=self.request.user.id)
        object_list = Project.objects.filter(company=user_profile.company)
        context['object_list'] = object_list
        context['amount'] = len(object_list)
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    template_name = os.path.join('projects', 'form.html')
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        user_profile = Profile.objects.get(user=self.request.user.id)
        form.instance.company = user_profile.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Projekt - skapa"
        return context


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = os.path.join('projects', 'detail.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = ProductForProject.objects.filter(project=self.object)
        context['product_list'] = product_list
        return context


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = os.path.join('projects', 'form.html')
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Projekt - ändra"
        return context


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = '/project'
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'Projekt',
            'url_name': 'project',
            'object_title': self.object.title,
            'object_return_id': self.object.id
        }
        return ctx



    def delete(self, request, *args, **kwargs):
        material = Project.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Projekt borttaget - "' + material.title + '"')
        return super(ProjectDelete, self).delete(request, *args, **kwargs)


# ProductFor Project
class ProductForProjectCreate(LoginRequiredMixin, CreateView):
    model = ProductForProject
    template_name = os.path.join('projects', 'form.html')
    fields = ['product', 'quantity']

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_object = Project.objects.get(pk=self.kwargs['project_id'])
        context['object'] = main_object
        context['form_header'] = "Lägg till produkt"
        return context


class ProductForProjectDelete(LoginRequiredMixin, DeleteView):
    model = ProductForProject
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.product.id})

    def delete(self, request, *args, **kwargs):
        product_for_project = ProductForProject.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Produkt bortagen - ' + product_for_project.product.title)
        return super(ProductForProjectDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        product_for_project = ProductForProject.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['header'] = 'Produkt för projekt'
        context['url_name'] = 'project'
        context['object_title'] = product_for_project.product.title
        context['object'] = product_for_project.project
        return context


class ProjektBoard(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('projects', 'board.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['states'] = list(ProjectState.objects.filter(company=Profile.objects.get(user=self.request.user.id).company))
        return context
