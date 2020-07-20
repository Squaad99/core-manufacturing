from django import forms

from company.models import ProjectState
from customers.models import Customer
from projects.models import Project


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(max_length=100, required=True, label="Title")
        self.fields['comment'] = forms.CharField(max_length=500, widget=forms.Textarea, required=False, label="Comment")
        project_states = ProjectState.objects.filter(company=self.company).order_by('index_position')
        self.fields['state'] = forms.ModelChoiceField(queryset=project_states, label="Stadie")
        customer_select_list = Customer.objects.filter(company=self.company).order_by('title')
        self.fields['customer'] = forms.ModelChoiceField(queryset=customer_select_list, label="Kund")

    class Meta:
        model = Project
        fields = (
            'title',
            'state',
            'customer',
            'comment'
        )
