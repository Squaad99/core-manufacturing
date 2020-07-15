import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from time_accounting.models import TimeReport, WorkReport


class TimeReportForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'type': 'date'}), label='Datum')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('project', css_class='form-group col mb-0'),
                Column('employee', css_class='form-group col mb-0'),
                Column('hours', css_class='form-group col mb-0'),
                Column('date', css_class='form-group col mb-0'),
                css_class='form-row'
            )
        )

    class Meta:
        model = TimeReport
        fields = ('project', 'employee', 'hours', 'date')


class TimeReportUpdateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Datum')

    class Meta:
        model = TimeReport
        fields = ('project', 'employee', 'hours', 'date')


class WorkReportForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Datum')
    time_start = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_end = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = WorkReport
        fields = ('employee', 'date', 'time_start', 'time_end')