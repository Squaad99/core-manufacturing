from django import forms

from company.models import ProjectState
from customers.models import Customer
from projects.models import Project


class ProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, label="Title")
    comment = forms.CharField(max_length=500, widget=forms.Textarea, required=False, label="Comment")
    state = forms.ModelChoiceField(queryset=ProjectState.objects.all(), label="Stadie")
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), label="Kund")
    
    class Meta:
        model = Project
        fields = (
            'title',
            'state',
            'customer',
            'comment'
        )