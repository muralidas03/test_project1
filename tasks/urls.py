from django.urls import path
from . import views

urlpatterns = [
    # Task Management
    path('', views.task_list, name='task_list'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('<int:task_id>/assign/', views.assign_task, name='assign_task'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/comment/', views.add_comment, name='add_comment'),
]
