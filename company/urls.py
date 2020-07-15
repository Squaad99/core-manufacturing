from django.urls import path

from company.views import CompanyProfileView, CompanyUpdate, EmployeeDelete, EmployeeUpdate, EmployeeCreate

urlpatterns = [
    path('', CompanyProfileView.as_view(), name='company-profile'),
    path('update/', CompanyUpdate.as_view(), name='company-profile-update'),
    # Employee
    path('create/', EmployeeCreate.as_view(), name='company-employee-create'),
    path('<int:pk>/update/', EmployeeUpdate.as_view(), name='company-employee-update'),
    path('<int:pk>/delete/', EmployeeDelete.as_view(), name='company-employee-delete'),
]