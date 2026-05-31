from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q
from tasks.models import Task

class DashboardCache(models.Model):
    """
    Cache model for dashboard statistics to improve performance
    """
    key = models.CharField(
        max_length=255,
        unique=True,
        help_text="Cache key identifier"
    )
    value = models.JSONField(
        help_text="Cached data in JSON format"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Cache expiration time"
    )
    
    class Meta:
        db_table = 'dashboard_cache'
        verbose_name = 'Dashboard Cache'
        verbose_name_plural = 'Dashboard Cache'
    
    def __str__(self):
        return self.key
    
    @classmethod
    def get_cache(cls, key):
        """Get cached data"""
        try:
            cache = cls.objects.get(key=key)
            return cache.value
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def set_cache(cls, key, value, expires_at=None):
        """Set cache data"""
        cache, created = cls.objects.update_or_create(
            key=key,
            defaults={'value': value, 'expires_at': expires_at}
        )
        return cache


class DashboardStatistics:
    """
    Statistics aggregator for dashboard
    """
    
    @staticmethod
    def get_total_users():
        return User.objects.count()
    
    @staticmethod
    def get_total_tasks():
        return Task.objects.count()
    
    @staticmethod
    def get_pending_tasks():
        return Task.objects.filter(status='pending').count()
    
    @staticmethod
    def get_in_progress_tasks():
        return Task.objects.filter(status='in_progress').count()
    
    @staticmethod
    def get_completed_tasks():
        return Task.objects.filter(status='completed').count()
    
    @staticmethod
    def get_overdue_tasks():
        from django.utils import timezone
        return Task.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress', 'on_hold']
        ).count()
    
    @staticmethod
    def get_user_task_statistics(user):
        """Get task statistics for a specific user"""
        return {
            'total': user.assigned_tasks.count(),
            'pending': user.assigned_tasks.filter(status='pending').count(),
            'in_progress': user.assigned_tasks.filter(status='in_progress').count(),
            'completed': user.assigned_tasks.filter(status='completed').count(),
            'overdue': DashboardStatistics._get_user_overdue_tasks(user),
        }
    
    @staticmethod
    def _get_user_overdue_tasks(user):
        from django.utils import timezone
        return user.assigned_tasks.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress', 'on_hold']
        ).count()
    
    @staticmethod
    def get_role_wise_statistics():
        """Get statistics grouped by role"""
        from roles.models import Role
        stats = {}
        for role in Role.objects.filter(is_active=True):
            user_count = role.users.filter(status='active').count()
            task_count = Task.objects.filter(
                assigned_to__profile__role=role
            ).count()
            stats[role.get_name_display()] = {
                'users': user_count,
                'tasks': task_count,
            }
        return stats
    
    @staticmethod
    def get_priority_wise_statistics():
        """Get statistics grouped by priority"""
        return {
            'low': Task.objects.filter(priority='low').count(),
            'medium': Task.objects.filter(priority='medium').count(),
            'high': Task.objects.filter(priority='high').count(),
            'urgent': Task.objects.filter(priority='urgent').count(),
        }
    
    @staticmethod
    def get_dashboard_context(user_role=None):
        """Get complete dashboard context"""
        return {
            'total_users': DashboardStatistics.get_total_users(),
            'total_tasks': DashboardStatistics.get_total_tasks(),
            'pending_tasks': DashboardStatistics.get_pending_tasks(),
            'in_progress_tasks': DashboardStatistics.get_in_progress_tasks(),
            'completed_tasks': DashboardStatistics.get_completed_tasks(),
            'overdue_tasks': DashboardStatistics.get_overdue_tasks(),
            'role_wise_stats': DashboardStatistics.get_role_wise_statistics(),
            'priority_wise_stats': DashboardStatistics.get_priority_wise_statistics(),
        }
