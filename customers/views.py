import os
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, CreateView, DetailView
from customers.models import Customer, ContactPerson
from django.contrib import messages

from users.models import Profile


class Overview(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = os.path.join('common', 'object_overview.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Kunder'
        context['url_name'] = 'customer'
        company = Profile.objects.get(user=self.request.user.id).company
        object_list = Customer.objects.filter(company=company)
        context['object_list'] = object_list
        context['amount'] = len(list(object_list))
        return context


class Create(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['title', 'web_address', 'comment']
    template_name = os.path.join('customers', 'form.html')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        user_profile = Profile.objects.get(user=self.request.user.id)
        form.instance.company = user_profile.company
        return super().form_valid(form)


class Detail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Customer
    contacts = ContactPerson.objects.filter()
    template_name = os.path.join('customers', 'detail.html')

    def has_permission(self):
        company = Profile.objects.get(user=self.request.user.id).company
        detail_object = self.get_object()
        if company == detail_object.company:
            return True
        return False

    def get_context_data(self, **kwargs):
        contacts = ContactPerson.objects.filter(customer=self.object)
        context = {
            'contacts': contacts,
            'object': self.object
        }
        return context


class Update(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['title', 'web_address', 'comment']
    template_name = os.path.join('customers', 'form.html')

    def form_valid(self, form):
        return super().form_valid(form)


class Delete(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = '/customer'
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'Kund',
            'url_name': 'customer',
            'object_title': self.object.title,
            'object_return_id': self.object.id
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Kund bortagen - "' + customer.title + '"')
        return super(Delete, self).delete(request, *args, **kwargs)


class ContactPersonCreate(LoginRequiredMixin, CreateView):
    model = ContactPerson
    fields = ['name', 'phone', 'email']
    template_name = os.path.join('customers', 'form.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_person'] = True
        main_object = Customer.objects.get(pk=self.kwargs['customer_id'])
        context['object'] = main_object
        return context

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(pk=self.kwargs['customer_id'])
        return super().form_valid(form)


class ContactPersonUpdate(LoginRequiredMixin, UpdateView):
    model = ContactPerson
    fields = ['name', 'phone', 'email']
    template_name = os.path.join('customers', 'form.html')


class ContactPersonDelete(LoginRequiredMixin, DeleteView):
    model = ContactPerson
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.customer.id})

    def get_context_data(self, **kwargs):
        contact_person = ContactPerson.objects.get(pk=self.kwargs['pk'])
        ctx = {
            'header': 'Kontaktperson',
            'url_name': 'customer',
            'object_title': contact_person.name,
            'object_return_id': self.object.customer.id
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        contact_person = ContactPerson.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Kontaktperson bortagen - ' + contact_person.name)
        return super(ContactPersonDelete, self).delete(request, *args, **kwargs)
