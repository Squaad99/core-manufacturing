import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from products.forms import MaterialForProductForm, WorkTaskForm
from products.models import Product, MaterialForProduct, WorkTask


class ProductOverview(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = os.path.join('common', 'object_overview.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Produkt'
        context['url_name'] = 'product'
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'extra_cost', 'comment']
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = os.path.join('products', 'detail.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materials = MaterialForProduct.objects.filter(product=self.object)
        context['material_list'] = materials

        material_total_cost = 0

        for material in list(materials):
            material_total_cost += material.material.base_cost
            if material.material.scalable_cost:
                material_total_cost += material.material.unit_cost * material.units
        context['total_material_cost'] = material_total_cost

        work_tasks = WorkTask.objects.filter(product=self.object)
        context['work_task_list'] = work_tasks

        work_tasks_hours = 0
        for work_task in list(work_tasks):
            work_tasks_hours += work_task.work_hours

        context['work_tasks_hours'] = work_tasks_hours

        return context


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'extra_cost', 'comment']
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        return super().form_valid(form)


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/product'
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Produkt'
        context['url_name'] = 'product'
        return context

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
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['header'] = 'Material för produkt'
        context['url_name'] = 'product'
        return context


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
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['header'] = 'Arbete för produkt'
        context['url_name'] = 'product'
        return context
