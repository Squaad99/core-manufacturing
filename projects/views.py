import logging
import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from company.models import ProjectState
from products.models import MaterialForProduct, WorkTaskForProduct
from products.utils import calculate_product_summary
from projects.form import ProjectForm
from projects.models import Project, ProductForProject
from projects.utils import calculate_project
from users.models import Profile


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
    fields = ['title', 'state', 'customer', 'comment']
    template_name = os.path.join('projects', 'form.html')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        company = Profile.objects.get(user=self.request.user.id).company
        form.instance.company = company
        return super(ProjectCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Projekt - skapa"
        context['form'] = ProjectForm(company=company)
        return context


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'state', 'customer', 'comment']
    template_name = os.path.join('projects', 'form.html')

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Projekt - ändra"
        context['form'] = ProjectForm(company=company, instance=self.object)
        return context


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = os.path.join('projects', 'detail.html')

    def has_permission(self):
        company = Profile.objects.get(user=self.request.user.id).company
        detail_object = self.get_object()
        if company == detail_object.company:
            return True
        return False

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        product_for_project_list = ProductForProject.objects.filter(project=self.object)
        calculate_products = []
        all_products_material_cost = 0
        all_products_work_cost = 0
        all_products_work_hours = 0
        for product_for_project in product_for_project_list:
            product_summary = calculate_product_summary(product_for_project.product)
            quantity = product_for_project.quantity
            all_products_material_cost += (product_summary.material_cost * quantity)
            all_products_work_cost += (product_summary.work_cost * quantity)
            all_products_work_hours += (product_summary.work_hours * quantity)
            calculate_products.append(
                {
                    'title': product_for_project.product.title,
                    'cost': (product_summary.total_cost * quantity),
                    'work_hours': (product_summary.work_hours * quantity),
                    'quantity': quantity,
                    'id': product_for_project.id
                }
            )

        return {
            'product_list': calculate_products,
            'object': self.object,
            'all_products_material_cost': all_products_material_cost,
            'all_products_work_cost': all_products_work_cost,
            'all_products_work_hours': all_products_work_hours,
            'total_cost': (all_products_material_cost + all_products_work_cost),
            'currency': company.currency
        }


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


# Product for Project
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
        return reverse('project-detail', kwargs={'pk': self.object.project.id})

    def delete(self, request, *args, **kwargs):
        product_for_project = ProductForProject.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Produkt bortagen - ' + product_for_project.product.title)
        return super(ProductForProjectDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'produkt för projekt',
            'url_name': 'project',
            'object_title': self.object.product.title,
            'object_return_id': self.object.project.id
        }
        return ctx


# Project board
class ProjektBoard(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('projects', 'board.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Profile.objects.get(user=self.request.user.id).company
        project_states = list(ProjectState.objects.filter(company=company))
        project_states.sort(key=lambda x: x.index_position)

        project_state_list = []

        for project_state in project_states:
            if project_state.display_table:
                total_work_hours = 0
                projects = list(Project.objects.filter(company=company, state=project_state))
                for project in projects:
                    project_summary = calculate_project(project)
                    total_work_hours += project_summary.total_hours
                    project.summary = project_summary

                project_state_list.append([project_state, projects, len(projects), total_work_hours])

        context['states'] = project_state_list
        return context
