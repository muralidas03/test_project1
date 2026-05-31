from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Role, Permission
from .forms import RoleForm, PermissionForm, RoleFilterForm
from users.rbac import admin_required

@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def role_list(request):
    """List all roles with filter"""
    roles = Role.objects.prefetch_related('permissions').all()
    form = RoleFilterForm(request.GET)
    
    if request.GET:
        name_filter = request.GET.get('name')
        is_active = request.GET.get('is_active')
        
        if name_filter:
            roles = roles.filter(name=name_filter)
        
        if is_active == 'true':
            roles = roles.filter(is_active=True)
        elif is_active == 'false':
            roles = roles.filter(is_active=False)
    
    paginator = Paginator(roles, 10)
    page = request.GET.get('page', 1)
    roles_page = paginator.get_page(page)
    
    context = {
        'roles': roles_page,
        'form': form,
        'total_roles': paginator.count,
    }
    return render(request, 'roles/role_list.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET"])
def role_detail(request, role_id):
    """View role details and permissions"""
    role = get_object_or_404(Role, id=role_id)
    permissions = role.permissions.all().order_by('permission')
    users = role.users.select_related('user').filter(status='active')
    
    paginator = Paginator(users, 10)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    
    context = {
        'role': role,
        'permissions': permissions,
        'users': users_page,
        'total_users': paginator.count,
    }
    return render(request, 'roles/role_detail.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def create_role(request):
    """Create new role"""
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            permissions = form.cleaned_data.get('permissions', [])
            for permission in permissions:
                role.permissions.add(permission)
            messages.success(request, f'Role {role.get_name_display()} created successfully.')
            return redirect('role_detail', role_id=role.id)
    else:
        form = RoleForm()
    
    context = {
        'form': form,
        'title': 'Create Role',
    }
    return render(request, 'roles/create_role.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def edit_role(request, role_id):
    """Edit role"""
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            # Update permissions
            role.permissions.clear()
            permissions = form.cleaned_data.get('permissions', [])
            for permission in permissions:
                role.permissions.add(permission)
            messages.success(request, f'Role {role.get_name_display()} updated successfully.')
            return redirect('role_detail', role_id=role.id)
    else:
        form = RoleForm(instance=role)
    
    context = {
        'form': form,
        'role': role,
        'title': f'Edit {role.get_name_display()}',
    }
    return render(request, 'roles/edit_role.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["POST"])
def delete_role(request, role_id):
    """Delete role"""
    role = get_object_or_404(Role, id=role_id)
    role_name = role.get_name_display()
    role.delete()
    messages.success(request, f'Role {role_name} deleted successfully.')
    return redirect('role_list')


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def manage_permissions(request, role_id):
    """Manage permissions for a role"""
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        permission_id = request.POST.get('permission_id')
        action = request.POST.get('action')  # 'add' or 'remove'
        
        if action == 'add':
            permission = Permission.objects.get(id=permission_id)
            role.permissions.add(permission)
            messages.success(request, f'Permission {permission.get_permission_display()} added.')
        elif action == 'remove':
            permission = Permission.objects.get(id=permission_id)
            role.permissions.remove(permission)
            messages.success(request, f'Permission {permission.get_permission_display()} removed.')
        
        return redirect('manage_permissions', role_id=role.id)
    
    assigned_permissions = role.permissions.all()
    all_permissions = Permission.objects.filter(role=role)
    
    context = {
        'role': role,
        'assigned_permissions': assigned_permissions,
        'all_permissions': all_permissions,
    }
    return render(request, 'roles/manage_permissions.html', context)
