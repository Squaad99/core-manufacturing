import datetime
import locale
import os
from calendar import monthrange
from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView, ListView
from time_accounting.filters import TimeReportFilter
from time_accounting.forms import TimeReportForm, TimeReportUpdateForm, WorkReportForm
from time_accounting.models import TimeReport, WorkReport
from time_accounting.utils import setup_calendar
from users.models import Profile


class TimeReportCreate(LoginRequiredMixin, CreateView):
    model = TimeReport
    template_name = os.path.join("time_accounting", 'time_report_form.html')
    form_class = TimeReportForm

    def form_valid(self, form):
        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        return super().form_valid(form)

    def get_context_data(self):
        company = Profile.objects.get(user=self.request.user.id).company
        time_report_list = TimeReport.objects.filter(company=company)

        employees = []
        hours = 0
        for report in time_report_list:
            hours += report.hours
            if report.employee not in employees:
                employees.append(str(report.employee))

        employees_string = ', '.join(employees)

        return {
            'time_report_list': time_report_list,
            'form': TimeReportForm,
            'employees': employees_string,
            'hours': hours,
            'filter_time_report': TimeReportFilter(self.request.GET, queryset=time_report_list)
        }

    def get_success_url(self, **kwargs):
        full_params = '?employee=' + self.request.GET['employee'] + "&date=" + self.request.GET['date'] + "&start_date=" \
                      + self.request.GET['start_date'] + "&end_date=" + self.request.GET['end_date']
        return reverse('time-overview') + full_params


class TimeReportUpdate(LoginRequiredMixin, UpdateView):
    model = TimeReport
    template_name = os.path.join("time_accounting", 'update_form.html')
    form_class = TimeReportUpdateForm
    success_url = '/time'


class TimeReportDelete(LoginRequiredMixin, DeleteView):
    model = TimeReport
    template_name = os.path.join('common', 'confirm_delete.html')
    success_url = "/time"

    def get_context_data(self, **kwargs):
        ctx = {
            'header': 'Tidrapport',
            'url_name': 'time-overview',
            'object_title': 'Tidrapport'
        }
        return ctx

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Tidrapport borttagen')
        return super(TimeReportDelete, self).delete(request, *args, **kwargs)


class TimeCalendarOverView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('time_accounting', 'calendar', 'calendar_overview.html')

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        calendar = setup_calendar(**kwargs)

        return {
            'current_date': calendar.selected_month,
            'month_name': calendar.selected_month.strftime('%B').capitalize(),
            'previous_name': calendar.previous_month_date.strftime('%B').capitalize(),
            'previous_month': calendar.previous_month,
            'next_name': calendar.next_month_date.strftime('%B').capitalize(),
            'next_month': calendar.next_month,
            'week_rows': calendar.week_rows
        }


class TimeCalendarDate(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('time_accounting', 'calendar', 'calendar_date_view.html')

    def get_context_data(self, **kwargs):
        company = Profile.objects.get(user=self.request.user.id).company
        selected_date = dt.now()
        if 'selected_date' in kwargs:
            divided = kwargs['selected_date'].split('-')
            selected_date = datetime.datetime(int(divided[0]), int(divided[1]), int(divided[2]))

        ctx = super().get_context_data(**kwargs)
        work_report_list = WorkReport.objects.filter(company=company, date=selected_date)
        ctx['work_report_list'] = work_report_list
        ctx['selected_date'] = selected_date.date()
        return ctx


class WorkReportCreate(LoginRequiredMixin, CreateView):
    model = WorkReport
    template_name = os.path.join('time_accounting', 'calendar', 'calendar_form.html')
    form_class = WorkReportForm
    success_url = "/time/calendar/overview/"

    def form_valid(self, form):
        if form.instance.time_start > form.instance.time_end:
            messages.error(self.request, "Starttid måste vara tidigare än sluttid.", extra_tags=" alert-danger")
            return super().form_invalid(form)

        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        form.instance.active = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Skapa - Arbetad tid"
        return context


