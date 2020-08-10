import datetime
import locale
from calendar import monthrange
from datetime import datetime as dt


class CalendarObject:

    def __init__(self, selected_month, month_range, previous_month_date, previous_month, next_month_date, next_month,
                 week_rows):
        self.selected_month = selected_month
        self.month_range = month_range
        self.previous_month_date = previous_month_date
        self.previous_month = previous_month
        self.next_month_date = next_month_date
        self.next_month = next_month
        self.week_rows = week_rows


def setup_calendar(**kwargs):
    if 'selected_month' in kwargs:
        input_date = kwargs['selected_month'].split('-')
        selected_month = datetime.datetime(int(input_date[0]), int(input_date[1]), 1)
    else:
        selected_month = dt.now()

    locale.setlocale(locale.LC_TIME, "sv_SE.utf8")
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
            week.append({'date': selected_month.replace(day=date_of_month),
                         'date_only': selected_month.replace(day=date_of_month).date(), 'current_month': True})
            date_of_month += 1
            if len(week) == 7:
                break
    week_rows.append(week)

    while True:
        week = []
        next_month_date_count = 1
        for i in range(0, 7):
            if date_of_month <= month_range[1]:
                week.append({'date': selected_month.replace(day=date_of_month),
                             'date_only': selected_month.replace(day=date_of_month).date(), 'current_month': True})
                date_of_month += 1
            else:
                week.append({'date': next_month_date_count, 'current_month': False})
                next_month_date_count += 1
        week_rows.append(week)
        if date_of_month > month_range[1]:
            break

    previous_month = str(previous_month_date.year) + "-" + str(previous_month_date.month)
    next_month = str(next_month_date.year) + "-" + str(next_month_date.month)

    return CalendarObject(selected_month, month_range, previous_month_date, previous_month, next_month_date, next_month,
                          week_rows)


def calculate_hours(workReport):
    hour = workReport.time_end.hour - workReport.time_start.hour
    minute = workReport.time_end.minute - workReport.time_start.minute
    if minute < 0:
        minute = (minute + 60)
        hour -= 1
    hour_percentage = (minute / 60)
    workReport.worked_hours = hour + round(hour_percentage, 1)


class WorkListSummary:
    def __init__(self, length, total, employees):
        self.length = length
        self.total = total
        self.employees = employees


def calculate_work_report_list(work_report_list):
    total_hours = 0
    employees = []
    for work_report in work_report_list:
        calculate_hours(work_report)
        total_hours += work_report.worked_hours
        if work_report.employee not in employees:
            employees.append(work_report.employee)
    return WorkListSummary(len(work_report_list), round(total_hours, 2), employees)
