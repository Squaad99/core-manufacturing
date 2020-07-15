
import django_filters
from django.db import models
from django.forms import DateInput
from django_filters import FilterSet
from time_accounting.models import TimeReport
from django.utils.translation import ugettext as _


class TimeReportFilter(FilterSet):
    choices = [
        ('today', _('Idag')),
        ('yesterday', _('Igår')),
        ('week', _('7 dagar')),
        ('month', _('Denna månad')),
        ('year', _('Detta år')),
    ]
    date = django_filters.DateRangeFilter(choices=choices, initial="Igår")
    start_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), field_name='start_date', lookup_expr='lt', label='Start datum')
    end_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), field_name='end_date', lookup_expr='gt', label='Slut datum')

    class Meta:
        model = TimeReport
        fields = ['employee']

    def filter_queryset(self, queryset):
        custom_filters = {}
        for name, value in self.form.cleaned_data.items():
            if name == 'start_date' or name == 'end_date':
                custom_filters.update({name: value})
        del self.form.cleaned_data['start_date']
        del self.form.cleaned_data['end_date']

        for name, value in self.form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, models.QuerySet), \
                "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)

        if custom_filters['start_date'] and custom_filters['end_date']:
            queryset = queryset.filter(date__range=[custom_filters['start_date'], custom_filters['end_date']])
        return queryset
