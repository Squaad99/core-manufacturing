import os
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, CreateView, DetailView
from customers.models import Customer, ContactPerson
from django.contrib import messages


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = os.path.join('customers', 'customer_list.html')
    context_object_name = 'customers'


class CustomerOverview(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = os.path.join('common', 'object_overview.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Kunder'
        context['url_name'] = 'customer'
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['title', 'web_address', 'comment']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    contacts = ContactPerson.objects.filter()

    def get_context_data(self, **kwargs):
        customer = kwargs['object']
        contacts = ContactPerson.objects.filter(customer=customer)

        context = {
            'contacts': contacts,
            'object': customer
        }
        return context


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['title', 'web_address', 'comment']

    def form_valid(self, form):
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Customer
    success_url = '/customer'

    def test_func(self):
        return True

    def delete(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Kund bortagen - "' + customer.title + '"')
        return super(CustomerDeleteView, self).delete(request, *args, **kwargs)


class ContactPersonCreateView(LoginRequiredMixin, CreateView):
    model = ContactPerson
    fields = ['name', 'phone', 'email']

    def get(self, request, *args, **kwargs):
        return super(ContactPersonCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(pk=self.kwargs['customer_id'])
        return super().form_valid(form)


class ContactPersonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ContactPerson

    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.customer.id})

    def test_func(self):
        return True

    def delete(self, request, *args, **kwargs):
        contact_person = ContactPerson.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Kontaktperson bortagen - ' + contact_person.name)
        return super(ContactPersonDeleteView, self).delete(request, *args, **kwargs)
