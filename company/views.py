import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, DeleteView, TemplateView

from company.models import Employee, ProjectState, ProjectType
from users.models import Company, Profile


class CompanyProfileView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('company', 'company_profile.html')
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Profile.objects.get(user=self.request.user.id).company
        context['company'] = company
        context['employee_list'] = Employee.objects.filter(company=company)
        project_state_list = list(ProjectState.objects.filter(company=company))
        project_state_list.sort(key=lambda x: x.index_position)
        context['project_state_list'] = project_state_list
        project_state_list = ProjectType.objects.filter(company=company)
        context['project_type_list'] = project_state_list
        context['object'] = company
        context['id'] = company.id
        return context


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['currency', 'cost_per_work_hour']
    template_name = os.path.join('company', 'form.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Ändra företag"
        return context

    def get_object(self):
        return Profile.objects.get(user=self.request.user.id).company


class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = os.path.join("company", 'table_form.html')
    fields = ['title']
    success_url = "/company"

    def form_valid(self, form):
        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anställd'
        return context


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = os.path.join("company", 'table_form.html')
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anställd'
        return context


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = os.path.join('common', 'confirm_delete.html')
    success_url = "/company"

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        ctx = {
            'header': 'Anställd',
            'url_name': 'company-profile',
            'object_title': employee.title
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Anställd bortagen - ' + employee.title)
        return super(EmployeeDelete, self).delete(request, *args, **kwargs)


# Project
class ProjectStateCreate(LoginRequiredMixin, CreateView):
    model = ProjectState
    template_name = os.path.join("company", 'table_form.html')
    fields = ['title', 'index_position', 'display_table']
    success_url = "/company/?tab=2"

    def form_valid(self, form):
        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Projekt stadie'
        context['tab'] = '2'
        return context


class ProjectStateUpdate(LoginRequiredMixin, UpdateView):
    model = ProjectState
    template_name = os.path.join("company", 'table_form.html')
    fields = ['title', 'index_position', 'display_table']
    success_url = "/company/?tab=2"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Projekt stadie'
        context['tab'] = '2'
        return context


class ProjectStateDelete(LoginRequiredMixin, DeleteView):
    model = ProjectState
    template_name = os.path.join('common', 'confirm_delete.html')
    success_url = "/company/?tab=2"

    def get_context_data(self, **kwargs):
        project_state = ProjectState.objects.get(pk=self.kwargs['pk'])
        ctx = {
            'header': 'Projekt stadie',
            'url_name': 'company-profile',
            'object_title': project_state.title,
            'tab': '2'
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        project_state = ProjectState.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Projekt stadie bortaget - ' + project_state.title)
        return super(ProjectStateDelete, self).delete(request, *args, **kwargs)


class ProjectTypeCreate(LoginRequiredMixin, CreateView):
    model = ProjectType
    template_name = os.path.join("company", 'table_form.html')
    fields = ['title']
    success_url = "/company/?tab=2"

    def form_valid(self, form):
        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Projekt typ'
        context['tab'] = '2'
        return context


class ProjectTypeUpdate(LoginRequiredMixin, UpdateView):
    model = ProjectType
    template_name = os.path.join("company", 'table_form.html')
    fields = ['title']
    success_url = "/company/?tab=2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Projekt typ'
        context['tab'] = '2'
        return context


class ProjectTypeDelete(LoginRequiredMixin, DeleteView):
    model = ProjectType
    template_name = os.path.join('common', 'confirm_delete.html')
    success_url = "/company/?tab=2"

    def get_context_data(self, **kwargs):
        project_type = ProjectType.objects.get(pk=self.kwargs['pk'])
        ctx = {
            'header': 'Projekt typ',
            'url_name': 'company-profile',
            'object_title': project_type.title,
            'tab': '2'
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        project_type = ProjectType.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Projekt typ bortaget - ' + project_type.title)
        return super().delete(request, *args, **kwargs)
