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
        if 'selected_month' in kwargs:
            input_date = kwargs['selected_month'].split('-')
            selected_month = datetime.datetime(int(input_date[0]), int(input_date[1]), 1)
        else:
            selected_month = dt.now()
        company = Profile.objects.get(user=self.request.user.id).company
        locale.setlocale(locale.LC_TIME, "sv_SE")
        month_range = monthrange(selected_month.year, selected_month.month)
        previous_month_date = selected_month.replace(day=1) - datetime.timedelta(days=1)
        next_month_date = selected_month.replace(day=month_range[1]) + datetime.timedelta(days=1)

        date_of_month = 1
        week_rows = []

        week = []

        if not month_range[0] == 0:
            previous_month_range = monthrange(previous_month_date.year, previous_month_date.month)
            last_date = previous_month_range[1]
            for i in range(0, month_range[0]):
                week.append({'date': last_date - i, 'current_month': False})
            week.reverse()
            while True:
                week.append({'date': selected_month.replace(day=date_of_month), 'current_month': True})
                date_of_month += 1
                if len(week) == 7:
                    break
        week_rows.append(week)

        while True:
            week = []
            next_month_date_count = 1
            for i in range(0, 7):
                if date_of_month <= month_range[1]:
                    week.append({'date': selected_month.replace(day=date_of_month), 'current_month': True})
                    date_of_month += 1
                else:
                    week.append({'date': next_month_date_count, 'current_month': False})
                    next_month_date_count += 1
            week_rows.append(week)
            if date_of_month > month_range[1]:
                break

        previous_month = str(previous_month_date.year) + "-" + str(previous_month_date.month)
        next_month = str(next_month_date.year) + "-" + str(next_month_date.month)

        return {
            'current_date': selected_month,
            'month_name': selected_month.strftime('%B').capitalize(),
            'previous_name': previous_month_date.strftime('%B').capitalize(),
            'previous_month': previous_month,
            'next_name': next_month_date.strftime('%B').capitalize(),
            'next_month': next_month,
            'week_rows': week_rows
        }


class WorkReportCreate(LoginRequiredMixin, CreateView):
    model = WorkReport
    template_name = os.path.join('time_accounting', 'calendar', 'calendar_form.html')
    form_class = WorkReportForm
    success_url = "/time/calendar/overview/"

    def form_valid(self, form):
        form.instance.company = Profile.objects.get(user=self.request.user.id).company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_header'] = "Skapa - Arbetad tid"
        return context


class WorkReportDate(LoginRequiredMixin, ListView):
    template_name = os.path.join('time_accounting', 'calendar', 'time_report_date.html')
    model = TimeReport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Profile.objects.get(user=self.request.user.id).company
        time_report_list = TimeReport.objects.filter(company=company)
        return context
