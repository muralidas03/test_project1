from django.urls import path
from . import views

urlpatterns = [
    # Role Management
    path('', views.role_list, name='role_list'),
    path('create/', views.create_role, name='create_role'),
    path('<int:role_id>/', views.role_detail, name='role_detail'),
    path('<int:role_id>/edit/', views.edit_role, name='edit_role'),
    path('<int:role_id>/delete/', views.delete_role, name='delete_role'),
    path('<int:role_id>/permissions/', views.manage_permissions, name='manage_permissions'),
]
