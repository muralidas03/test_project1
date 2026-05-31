from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile
    path('profile/', views.user_profile, name='user_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # User Management (Admin only)
    path('list/', views.user_list, name='user_list'),
    path('create/', views.create_user, name='create_user'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # View users by role
    path('role/<str:role_name>/', views.users_by_role, name='users_by_role'),
]
