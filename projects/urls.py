from django.urls import path
from .views import ProjectOverview, ProjectCreate, ProjectDetail, ProjectUpdate, ProjectDelete, \
    ProductForProjectCreate, ProductForProjectDelete, ProjektBoard

urlpatterns = [
    path('', ProjectOverview.as_view(), name='project-overview'),
    path('new/', ProjectCreate.as_view(), name='project-create'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('<int:pk>/update/', ProjectUpdate.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path('<int:project_id>/productForProject/add/', ProductForProjectCreate.as_view(), name='project-product-add'),
    path('<int:pk>/productForProject/delete/', ProductForProjectDelete.as_view(), name='project-product-delete'),
    path('board/', ProjektBoard.as_view(), name='project-board')
]