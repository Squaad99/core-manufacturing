import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from materials.form import MaterialForm
from materials.models import Material
from users.models import Profile


class MaterialOverview(LoginRequiredMixin, ListView):
    model = Material
    context_object_name = 'materials'
    template_name = os.path.join('common', 'object_overview.html')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['header'] = 'Material'
        ctx['url_name'] = 'material'
        company = Profile.objects.get(user=self.request.user.id).company
        object_list = Material.objects.filter(company=company)
        ctx['object_list'] = object_list
        ctx['amount'] = len(list(object_list))
        return ctx


class MaterialCreate(LoginRequiredMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = os.path.join('materials', 'form.html')

    def form_valid(self, form):
        if not form.instance.scalable_cost:
            form.instance.unit_label = "Enhet"
            form.instance.unit_cost = 0
        form.instance.created_by = self.request.user
        user_profile = Profile.objects.get(user=self.request.user.id)
        form.instance.company = user_profile.company
        return super().form_valid(form)


class MaterialDetail(LoginRequiredMixin, DetailView):
    model = Material
    template_name = os.path.join('materials', 'detail.html')


class MaterialUpdate(LoginRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = os.path.join('materials', 'form.html')


class MaterialDelete(LoginRequiredMixin, DeleteView):
    model = Material
    success_url = '/material'
    template_name = os.path.join('common', 'confirm_delete.html')

    def get_context_data(self, **kwargs):
        return {
            'header': 'Material',
            'url_name': 'material',
            'object_title': self.object.title,
            'object_return_id': self.object.id
        }

    def delete(self, request, *args, **kwargs):
        material = Material.objects.get(pk=kwargs['pk'])
        messages.info(self.request, 'Material borttaget - "' + material.title + '"')
        return super(MaterialDelete, self).delete(request, *args, **kwargs)
