from django.urls import path

from .views import MaterialOverview, MaterialCreate, MaterialDetail, MaterialUpdate, MaterialDelete

urlpatterns = [
    path('', MaterialOverview.as_view(), name='material-overview'),
    path('material/create/', MaterialCreate.as_view(), name='material-create'),
    path('material/<int:pk>/', MaterialDetail.as_view(), name='material-detail'),
    path('<int:pk>/update/', MaterialUpdate.as_view(), name='material-update'),
    path('<int:pk>/delete/', MaterialDelete.as_view(), name='material-delete')
]
