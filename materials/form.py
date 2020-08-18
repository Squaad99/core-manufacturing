from crispy_forms.helper import FormHelper
from django import forms

from materials.models import Material


class MaterialForm(forms.ModelForm):
    title = forms.CharField(label='Titel ', widget=forms.TextInput(attrs={'placeholder': 'Titel'}))
    base_cost = forms.FloatField(label='Bas kostnad ', initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Bas kostnad'}))
    scalable_cost = forms.BooleanField(initial=True, label='Skalbar kostnad (Enheter)', widget=forms.CheckboxInput(attrs={'id': 'scalable_cost_box'}), required=False)
    unit_label = forms.CharField(label='Enhetsnamn ', widget=forms.TextInput(attrs={'placeholder': 'Enhetsnamn', 'class': 'scalable_input'}), required=False)
    unit_cost = forms.FloatField(label='Kostnad per enhet ', initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Kostnad per enhet', 'class': 'scalable_input'}))
    comment = forms.CharField(label='Anteckning', widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = Material
        fields = ['title', 'base_cost', 'scalable_cost', 'unit_label', 'unit_cost', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
