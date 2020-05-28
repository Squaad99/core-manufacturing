from django.urls import path

from products.views import ProductOverview, ProductCreate, ProductDetail, ProductUpdate, ProductDelete, \
    MaterialForProductCreate, MaterialForProductDelete, WorkTaskCreate, WorkTaskDelete

urlpatterns = [
    path('', ProductOverview.as_view(), name='product-overview'),
    path('create/', ProductCreate.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('<int:product_id>/material/add/', MaterialForProductCreate.as_view(), name='material-for-product-add'),
    path('<int:pk>/contactPerson/delete/', MaterialForProductDelete.as_view(), name='material-for-product-delete'),
    path('<int:product_id>/workTask/add/', WorkTaskCreate.as_view(), name='work-task-add'),
    path('<int:pk>/workTask/delete/', WorkTaskDelete.as_view(), name='work-task-delete'),
]
