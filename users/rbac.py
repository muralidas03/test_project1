from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods

def permission_required(permission_code):
    """
    Decorator to check if user has specific permission
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper(request, *args, **kwargs):
            user_profile = request.user.profile
            if user_profile.has_permission(permission_code):
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access this resource.')
            return HttpResponseForbidden('Permission Denied')
        return wrapper
    return decorator


def role_required(role_name):
    """
    Decorator to check if user has specific role
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper(request, *args, **kwargs):
            user_profile = request.user.profile
            if user_profile.role and user_profile.role.name == role_name:
                return view_func(request, *args, **kwargs)
            messages.error(request, f'This page is only accessible to {role_name}s.')
            return HttpResponseForbidden('Permission Denied')
        return wrapper
    return decorator


def roles_required(*role_names):
    """
    Decorator to check if user has any of the specified roles
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper(request, *args, **kwargs):
            user_profile = request.user.profile
            if user_profile.role and user_profile.role.name in role_names:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access this resource.')
            return HttpResponseForbidden('Permission Denied')
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorator to check if user is admin
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        user_profile = request.user.profile
        if user_profile.is_admin():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'This page is only accessible to administrators.')
        return HttpResponseForbidden('Permission Denied')
    return wrapper


def user_owns_task(view_func):
    """
    Decorator to check if user owns/is assigned to a task
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, task_id, *args, **kwargs):
        from tasks.models import Task
        try:
            task = Task.objects.get(id=task_id)
            user_profile = request.user.profile
            
            # Allow if user is the creator, assignee, or admin
            if (task.created_by == request.user or 
                task.assigned_to == request.user or 
                user_profile.is_admin() or 
                user_profile.is_manager()):
                return view_func(request, task_id, *args, **kwargs)
            
            messages.error(request, 'You do not have permission to access this task.')
            return HttpResponseForbidden('Permission Denied')
        except Task.DoesNotExist:
            return redirect('task_list')
    return wrapper


class RBACMixin:
    """
    Mixin for class-based views to check permissions
    """
    required_permission = None
    required_role = None
    required_roles = None
    
    def dispatch(self, request, *args, **kwargs):
        user_profile = request.user.profile if hasattr(request.user, 'profile') else None
        
        if self.required_permission and user_profile:
            if not user_profile.has_permission(self.required_permission):
                messages.error(request, 'You do not have permission to access this resource.')
                return HttpResponseForbidden('Permission Denied')
        
        if self.required_role and user_profile:
            if not (user_profile.role and user_profile.role.name == self.required_role):
                messages.error(request, 'You do not have permission to access this resource.')
                return HttpResponseForbidden('Permission Denied')
        
        if self.required_roles and user_profile:
            if not (user_profile.role and user_profile.role.name in self.required_roles):
                messages.error(request, 'You do not have permission to access this resource.')
                return HttpResponseForbidden('Permission Denied')
        
        return super().dispatch(request, *args, **kwargs)


def get_user_permissions(user):
    """
    Get all permissions for a user based on their role
    """
    if hasattr(user, 'profile') and user.profile.role:
        return list(user.profile.role.get_permissions().values_list('permission', flat=True))
    return []


def check_permission(user, permission_code):
    """
    Check if user has specific permission
    """
    if hasattr(user, 'profile'):
        return user.profile.has_permission(permission_code)
    return False
