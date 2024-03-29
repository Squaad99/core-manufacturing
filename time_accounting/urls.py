from django.urls import path
from time_accounting.views import TimeReportCreate, TimeReportUpdate, TimeReportDelete, TimeCalendarOverView, \
    WorkReportCreate, TimeCalendarDate, WorkReportUpdate, WorkReportDelete

urlpatterns = [
    path('', TimeReportCreate.as_view(), name='time-overview'),
    path('<int:pk>/update/', TimeReportUpdate.as_view(), name='time-report-update'),
    path('<int:pk>/delete/', TimeReportDelete.as_view(), name='time-report-delete'),
    path('calendar/overview/', TimeCalendarOverView.as_view(), name='time-calendar-overview'),
    path('calendar/overview/<str:selected_month>/', TimeCalendarOverView.as_view(), name='time-calendar-overview'),
    path('calendar/dateview/<str:selected_date>/', TimeCalendarDate.as_view(), name='time-calendar-dateview'),
    path('calendar/new/', WorkReportCreate.as_view(), name='time-calendar-create'),
    path('calendar/update/<str:pk>', WorkReportUpdate.as_view(), name='time-calendar-update'),
    path('calendar/delete/<str:pk>', WorkReportDelete.as_view(), name='time-calendar-delete'),
]