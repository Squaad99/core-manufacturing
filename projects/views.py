import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from company.models import ProjectState
from products.models import MaterialForProduct, WorkTask
from products.utils import calculate_product_cost
from projects.form import ProjectForm
from projects.models import Project, ProductForProject
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
    template_name = os.path.join('projects', 'form.html')
    fields = ['title', 'state', 'customer', 'comment']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        company = Profile.objects.get(user=self.request.user.id).company
        form.instance.company = company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Projekt - skapa"
        context['form'] = ProjectForm(company=company)
        return context


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = os.path.join('projects', 'detail.html')

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        product_list = ProductForProject.objects.filter(project=self.object)
        calculate_products = []
        total_material_cost = 0
        total_work_hours = 0
        for product in product_list:
            materials = MaterialForProduct.objects.filter(product=product.product)
            work_tasks = WorkTask.objects.filter(product=product.product)
            cost_response = calculate_product_cost(materials, work_tasks, company, product.product)
            cost = (cost_response[0] * product.quantity)
            total_material_cost += cost
            work_hours = (cost_response[1] * product.quantity)
            total_work_hours += work_hours
            calculate_products.append(
                {
                    'title': product.product.title,
                    'cost': cost,
                    'work_hours': total_work_hours,
                    'quantity': product.quantity,
                    'id': product.id
                }
            )

        total_work_cost = (total_work_hours * company.cost_per_work_hour)
        total_cost = total_material_cost + total_work_cost

        return {
            'product_list': calculate_products,
            'object': self.object,
            'total_material_cost': total_material_cost,
            'total_work_hours': total_work_hours,
            'total_work_cost': total_work_cost,
            'total_cost': total_cost,
            'currency': company.currency
        }


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
                projects = Project.objects.filter(company=company, state=project_state)
                project_state_list.append([project_state, projects, total_work_hours])

        context['states'] = project_state_list
        return context
