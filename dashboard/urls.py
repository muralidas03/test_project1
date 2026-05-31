from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('statistics/', views.statistics, name='statistics'),
    path('user/<int:user_id>/statistics/', views.user_statistics, name='user_statistics'),
]
