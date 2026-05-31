from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import DashboardStatistics
from tasks.models import Task, TaskLog
from users.models import UserProfile
from roles.models import Role

@login_required(login_url='login')
@require_http_methods(["GET"])
def dashboard(request):
    """Main dashboard view - role-based"""
    user_profile = request.user.profile
    context = {
        'user': request.user,
        'user_profile': user_profile,
    }
    
    # Get common statistics for all users
    context.update({
        'total_tasks': Task.objects.count(),
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
        'completed_tasks': Task.objects.filter(status='completed').count(),
        'overdue_tasks': DashboardStatistics.get_overdue_tasks(),
    })
    
    # Role-specific dashboard
    if user_profile.is_admin():
        context.update(admin_dashboard_context(request))
    elif user_profile.is_manager():
        context.update(manager_dashboard_context(request))
    elif user_profile.is_team_lead():
        context.update(team_lead_dashboard_context(request))
    else:
        context.update(employee_dashboard_context(request))
    
    return render(request, 'dashboard/dashboard.html', context)


def admin_dashboard_context(request):
    """Get admin dashboard context"""
    context = {
        'total_users': UserProfile.objects.filter(status='active').count(),
        'total_roles': Role.objects.filter(is_active=True).count(),
        'role_wise_stats': DashboardStatistics.get_role_wise_statistics(),
        'priority_wise_stats': DashboardStatistics.get_priority_wise_statistics(),
        'recent_tasks': Task.objects.select_related('created_by', 'assigned_to').order_by('-created_at')[:10],
        'recent_logs': TaskLog.objects.select_related('task', 'performed_by').order_by('-created_at')[:15],
        'user_task_summary': get_user_task_summary(),
    }
    return context


def manager_dashboard_context(request):
    """Get manager dashboard context"""
    # Get team members (employees reporting to this manager)
    team_members = UserProfile.objects.filter(
        role__name='employee',
        status='active'
    )[:20]
    
    # Get team's tasks
    team_tasks = Task.objects.filter(
        assigned_to__profile__in=team_members
    )
    
    context = {
        'team_members_count': team_members.count(),
        'team_members': team_members,
        'team_tasks': team_tasks.count(),
        'team_completed_tasks': team_tasks.filter(status='completed').count(),
        'team_pending_tasks': team_tasks.filter(status='pending').count(),
        'role_wise_stats': DashboardStatistics.get_role_wise_statistics(),
        'team_tasks_list': team_tasks.select_related('created_by', 'assigned_to')[:10],
    }
    return context


def team_lead_dashboard_context(request):
    """Get team lead dashboard context"""
    user = request.user
    
    # Get team member tasks
    team_tasks = Task.objects.filter(
        assigned_to__profile__role__name='employee',
        created_by=user
    )
    
    context = {
        'my_created_tasks': Task.objects.filter(created_by=user).count(),
        'team_tasks': team_tasks.count(),
        'completed_team_tasks': team_tasks.filter(status='completed').count(),
        'pending_team_tasks': team_tasks.filter(status='pending').count(),
        'team_tasks_list': team_tasks.select_related('created_by', 'assigned_to')[:10],
    }
    return context


def employee_dashboard_context(request):
    """Get employee dashboard context"""
    user = request.user
    user_stats = DashboardStatistics.get_user_task_statistics(user)
    
    # Get recent activity
    recent_logs = TaskLog.objects.filter(task__assigned_to=user).order_by('-created_at')[:10]
    
    context = {
        'user_stats': user_stats,
        'my_tasks': user.assigned_tasks.all(),
        'my_pending_tasks': user.assigned_tasks.filter(status='pending').count(),
        'my_in_progress_tasks': user.assigned_tasks.filter(status='in_progress').count(),
        'my_completed_tasks': user.assigned_tasks.filter(status='completed').count(),
        'my_overdue_tasks': user_stats['overdue'],
        'recent_activity': recent_logs,
    }
    return context


def get_user_task_summary():
    """Get summary of tasks per user"""
    from django.db.models import Count, Q
    
    summary = User.objects.annotate(
        total_tasks=Count('assigned_tasks'),
        completed_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='completed')),
        pending_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='pending')),
    ).filter(
        is_active=True,
        total_tasks__gt=0
    ).order_by('-total_tasks')[:10]
    
    return summary


@login_required(login_url='login')
@require_http_methods(["GET"])
def statistics(request):
    """View detailed statistics and reports"""
    user_profile = request.user.profile
    
    # Check if user has permission to view reports
    if not (user_profile.is_admin() or user_profile.is_manager()):
        return render(request, 'dashboard/access_denied.html', status=403)
    
    context = {
        'total_users': UserProfile.objects.filter(status='active').count(),
        'total_tasks': Task.objects.count(),
        'completed_tasks': Task.objects.filter(status='completed').count(),
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'role_wise_stats': DashboardStatistics.get_role_wise_statistics(),
        'priority_wise_stats': DashboardStatistics.get_priority_wise_statistics(),
        'user_task_summary': get_user_task_summary(),
        'task_status_summary': get_task_status_summary(),
    }
    
    return render(request, 'dashboard/statistics.html', context)


def get_task_status_summary():
    """Get task count by status and priority"""
    from django.db.models import Count
    
    summary = {}
    for status, status_name in Task.STATUS_CHOICES:
        summary[status_name] = Task.objects.filter(status=status).count()
    
    return summary


@login_required(login_url='login')
@require_http_methods(["GET"])
def user_statistics(request, user_id):
    """View statistics for a specific user"""
    from users.models import UserProfile
    
    user_profile = UserProfile.objects.select_related('user', 'role').get(user_id=user_id)
    user_stats = DashboardStatistics.get_user_task_statistics(user_profile.user)
    
    # Get task breakdown
    tasks = user_profile.user.assigned_tasks.all()
    
    context = {
        'user_profile': user_profile,
        'user_stats': user_stats,
        'tasks': tasks,
        'task_breakdown': {
            'pending': tasks.filter(status='pending').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'completed': tasks.filter(status='completed').count(),
            'on_hold': tasks.filter(status='on_hold').count(),
        }
    }
    
    return render(request, 'dashboard/user_statistics.html', context)
