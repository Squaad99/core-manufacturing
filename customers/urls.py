from django.urls import path

from .views import CustomerCreateView, CustomerDetailView, CustomerUpdateView, CustomerDeleteView, \
    ContactPersonCreateView, ContactPersonDeleteView, CustomerOverview

urlpatterns = [
    path('', CustomerOverview.as_view(), name='customer-overview'),
    path('new/', CustomerCreateView.as_view(), name='customer-create'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('<int:customer_id>/contactPerson/new/', ContactPersonCreateView.as_view(), name='contactPerson-create'),
    path('<int:pk>/contactPerson/delete/', ContactPersonDeleteView.as_view(), name='contactPerson-delete'),
]
