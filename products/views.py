import os
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from products.forms import MaterialForProductForm, WorkTaskForm
from products.models import Product, MaterialForProduct, WorkTaskForProduct
from products.utils import calculate_product_summary
from users.models import Profile


class ProductOverview(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = os.path.join('common', 'object_overview.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Produkter'
        context['url_name'] = 'product'
        user_profile = Profile.objects.get(user=self.request.user.id)
        object_list = Product.objects.filter(company=user_profile.company)
        context['object_list'] = object_list
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'specification', 'comment']
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


class ProductDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = os.path.join('products', 'detail.html')

    def has_permission(self):
        company = Profile.objects.get(user=self.request.user.id).company
        detail_object = self.get_object()
        if company == detail_object.company:
            return True
        return False

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        ctx = super().get_context_data(**kwargs)
        ctx['product_summary'] = calculate_product_summary(self.object)
        ctx['company'] = company
        return ctx


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'specification', 'comment']
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
    fields = ['material', 'units']
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        company = Profile.objects.get(user=self.request.user.id).company
        form.instance.product = Product.objects.get(pk=self.kwargs['pk'])
        if not company == form.instance.material.company:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        main_object = Product.objects.get(pk=self.kwargs['pk'])
        context['object'] = main_object
        context['form_header'] = "Lägg till material"
        context['form'] = MaterialForProductForm(company=company)
        return context


class MaterialForProductUpdate(LoginRequiredMixin, UpdateView):
    model = MaterialForProduct
    fields = ['material', 'units']
    template_name = os.path.join('products', 'form.html')

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Material för produkt - ändra"
        context['object'] = self.object.product
        context['form'] = MaterialForProductForm(company=company, instance=self.object)
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
    model = WorkTaskForProduct
    fields = ['work_type', 'work_hours']
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs['product_id'])
        form.instance.product = product
        if not product.company == form.instance.work_type.company:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        main_object = Product.objects.get(pk=self.kwargs['product_id'])
        context['object'] = main_object
        context['form_header'] = "Lägg till arbete"
        context['form'] = WorkTaskForm(company=company)
        return context


class WorkTaskUpdate(LoginRequiredMixin, UpdateView):
    model = WorkTaskForProduct
    fields = ['work_type', 'work_hours']
    template_name = os.path.join('products', 'form.html')

    def form_valid(self, form):
        company = Profile.objects.get(user=self.request.user.id).company
        if not company == form.instance.material.company:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        context = super().get_context_data(**kwargs)
        context['object'] = self.object.product
        context['form_header'] = "Arbete för produkt - ändra"
        context['form'] = WorkTaskForm(company=company, instance=self.object)
        return context


class WorkTaskDelete(LoginRequiredMixin, DeleteView):
    model = WorkTaskForProduct
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.product.id})

    def delete(self, request, *args, **kwargs):
        work = WorkTaskForProduct.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Arbete bortaget - ' + work.work_type.title)
        return super(WorkTaskDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'Arbete för produkt',
            'url_name': 'product',
            'object_title': self.object.work_type,
            'object_return_id': self.object.product.id
        }
        return ctx

