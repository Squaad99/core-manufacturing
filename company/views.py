import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView

from company.models import Employee, ProjectState
from users.models import Company, Profile


class CompanyProfileView(LoginRequiredMixin, ListView):
    template_name = os.path.join('company', 'company_profile.html')
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Profile.objects.get(user=self.request.user.id).company
        context['employee_list'] = Employee.objects.filter(company=company)
        context['object'] = company
        context['id'] = company.id
        return context


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['currency', 'cost_per_work_hour']
    template_name = os.path.join('company', 'form.html')

    def form_valid(self, form):
        form_content = dict(self.request.POST)
        state_list = []
        for key in form_content:
            if "state" in key:
                state_list.append(form_content[key])

        if not state_list:
            messages.warning(self.request, 'Projekt stadier får inte lämnas tom.')
            return super().form_invalid(form)
        else:
            self.update_states(state_list)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Ändra företag"
        context['state_list'] = ProjectState.objects.filter(company=Profile.objects.get(user=self.request.user.id).company)
        return context

    def get_object(self):
        return Profile.objects.get(user=self.request.user.id).company

    def update_states(self, new_states):
        company = Profile.objects.get(user=self.request.user.id).company
        ProjectState.objects.filter(company=company).delete()
        index = 1
        for state in new_states:
            if type(state) == list:
                for state_inside in state:
                    ProjectState(company=company, title=state_inside, index_position=index).save()
                    index += 1
            else:
                ProjectState(company=company, title=state[0], index_position=index).save()
                index += 1


class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = os.path.join("company", 'employee_form.html')
    fields = ['title']
    success_url = "/company"

    def form_valid(self, form):
        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        return super().form_valid(form)


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = os.path.join("company", 'employee_form.html')
    fields = ['title']


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


