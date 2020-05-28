from django import forms

from materials.models import Material
from products.models import MaterialForProduct, WorkTask


class MaterialForProductForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all(), label="Material")
    units = forms.IntegerField(label="Enheter", initial=0, required=False)

    class Meta:
        model = MaterialForProduct
        fields = ['material', 'units']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WorkTaskForm(forms.ModelForm):
    title = forms.CharField(label="Arbete")
    work_hours = forms.FloatField(label="Timmar", initial=0, required=False)

    class Meta:
        model = WorkTask
        fields = ['title', 'work_hours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
