from django import forms

from company.models import WorkType
from materials.models import Material
from products.models import MaterialForProduct, WorkTaskForProduct


class MaterialForProductForm(forms.ModelForm):
    units = forms.IntegerField(label="Enheter", initial=0, required=False)

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(MaterialForProductForm, self).__init__(*args, **kwargs)
        material_list = Material.objects.filter(company=self.company).order_by('title')
        self.fields['material'] = forms.ModelChoiceField(queryset=material_list, label="Material")

    class Meta:
        model = MaterialForProduct
        fields = ['material', 'units']


class WorkTaskForm(forms.ModelForm):
    work_hours = forms.FloatField(label="Timmar", initial=0, required=False)

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(WorkTaskForm, self).__init__(*args, **kwargs)
        work_type_list = WorkType.objects.filter(company=self.company).order_by('title')
        self.fields['work_type'] = forms.ModelChoiceField(queryset=work_type_list, label="Arbetskategori")

    class Meta:
        model = WorkTaskForProduct
        fields = ['work_type', 'work_hours']
