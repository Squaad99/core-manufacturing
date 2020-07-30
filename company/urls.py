from django.urls import path

from company.views import CompanyProfileView, CompanyUpdate, EmployeeDelete, EmployeeUpdate, EmployeeCreate, \
    ProjectStateCreate, ProjectStateUpdate, ProjectStateDelete, ProjectTypeCreate, ProjectTypeUpdate, ProjectTypeDelete

urlpatterns = [
    path('', CompanyProfileView.as_view(), name='company-profile'),
    path('<int:tab>/', CompanyProfileView.as_view(), name='company-profile'),
    path('update/', CompanyUpdate.as_view(), name='company-profile-update'),
    # Employee
    path('employee/create/', EmployeeCreate.as_view(), name='company-employee-create'),
    path('employee/<int:pk>/update/', EmployeeUpdate.as_view(), name='company-employee-update'),
    path('employee/<int:pk>/delete/', EmployeeDelete.as_view(), name='company-employee-delete'),
    # Project State
    path('project-state/create/', ProjectStateCreate.as_view(), name='company-project-state-create'),
    path('project-state/<int:pk>/update/', ProjectStateUpdate.as_view(), name='company-project-state-update'),
    path('project-state/<int:pk>/delete/', ProjectStateDelete.as_view(), name='company-project-state-delete'),
    # Project type
    path('project-type/create/', ProjectTypeCreate.as_view(), name='company-project-type-create'),
    path('project-type/<int:pk>/update/', ProjectTypeUpdate.as_view(), name='company-project-type-update'),
    path('project-type/<int:pk>/delete/', ProjectTypeDelete.as_view(), name='company-project-type-delete'),
]