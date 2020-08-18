from django.urls import path

from .views import Update, Delete, ContactPersonCreate, ContactPersonDelete, Overview, Create, Detail, \
    ContactPersonUpdate

urlpatterns = [
    path('', Overview.as_view(), name='customer-overview'),
    path('new/', Create.as_view(), name='customer-create'),
    path('<int:pk>/', Detail.as_view(), name='customer-detail'),
    path('<int:pk>/update/', Update.as_view(), name='customer-update'),
    path('<int:pk>/delete/', Delete.as_view(), name='customer-delete'),
    path('<int:customer_id>/contactPerson/new/', ContactPersonCreate.as_view(), name='contactPerson-create'),
    path('<int:pk>/contactPerson/update/', ContactPersonUpdate.as_view(), name='contactPerson-update'),
    path('<int:pk>/contactPerson/delete/', ContactPersonDelete.as_view(), name='contactPerson-delete'),
]
