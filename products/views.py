import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from products.forms import MaterialForProductForm, WorkTaskForm
from products.models import Product, MaterialForProduct, WorkTask
from products.utils import calculate_product_cost
from users.models import Profile


class ProductOverview(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = os.path.join('common', 'object_overview.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Produkt'
        context['url_name'] = 'product'
        user_profile = Profile.objects.get(user=self.request.user.id)
        object_list = Product.objects.filter(company=user_profile.company)
        context['object_list'] = object_list
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'extra_cost', 'comment']
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        user_profile = Profile.objects.get(user=self.request.user.id)
        form.instance.company = user_profile.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Produkt - skapa"
        return context


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = os.path.join('products', 'detail.html')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        company = Profile.objects.get(user=self.request.user.id).company
        ctx['currency'] = company.currency
        materials = MaterialForProduct.objects.filter(product=self.object)
        ctx['material_list'] = materials

        work_tasks = WorkTask.objects.filter(product=self.object)
        ctx['work_task_list'] = work_tasks

        ctx['total_material_cost'], ctx['work_tasks_hours'], ctx['work_cost'], ctx['total_cost']= \
            calculate_product_cost(materials, work_tasks, company, self.object)
        return ctx


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'extra_cost', 'comment']
    template_name = os.path.join('products', 'form.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Produkt - ändra"
        return context


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/product'
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'Produkt',
            'url_name': 'product',
            'object_title': self.object.title,
            'object_return_id': self.object.id
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Produkt borttaget - "' + product.title + '"')
        return super(ProductDelete, self).delete(request, *args, **kwargs)


# Material
class MaterialForProductCreate(LoginRequiredMixin, CreateView):
    model = MaterialForProduct
    form_class = MaterialForProductForm
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs['product_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_object = Product.objects.get(pk=self.kwargs['product_id'])
        context['object'] = main_object
        context['form_header'] = "Lägg till material"
        return context


class MaterialForProductDelete(LoginRequiredMixin, DeleteView):
    model = MaterialForProduct
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.product.id})

    def delete(self, request, *args, **kwargs):
        material_for_product = MaterialForProduct.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Material bortaget - ' + material_for_product.material.title)
        return super(MaterialForProductDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        material = MaterialForProduct.objects.get(pk=self.kwargs['pk'])
        ctx = {
            'header': 'Material för produkt',
            'url_name': 'product',
            'object_title': material.material.title,
            'object_return_id': self.object.product.id
        }
        return ctx


# Work Task
class WorkTaskCreate(LoginRequiredMixin, CreateView):
    model = WorkTask
    form_class = WorkTaskForm
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs['product_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_object = Product.objects.get(pk=self.kwargs['product_id'])
        context['object'] = main_object
        context['form_header'] = "Lägg till arbete"
        return context


class WorkTaskDelete(LoginRequiredMixin, DeleteView):
    model = WorkTask
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.product.id})

    def delete(self, request, *args, **kwargs):
        work_task = WorkTask.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Arbete bortaget - ' + work_task.title)
        return super(WorkTaskDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'Arbete för produkt',
            'url_name': 'product',
            'object_title': self.object.title,
            'object_return_id': self.object.product.id
        }
        return ctx

