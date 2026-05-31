from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import UserProfile
from .forms import (
    UserRegistrationForm, UserProfileForm, UserSearchForm, ChangePasswordForm
)
from .rbac import admin_required, roles_required
from roles.models import Role

@require_http_methods(["GET", "POST"])
def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.profile.status == 'active':
                login(request, user)
                # Update last login tracked
                user.profile.last_login_tracked = timezone.now()
                user.profile.save(update_fields=['last_login_tracked'])
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Your account is inactive. Contact administrator.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


@login_required(login_url='login')
@require_http_methods(["GET"])
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def user_profile(request):
    """User profile view"""
    user_profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def change_password(request):
    """Change password view"""
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['old_password']):
                messages.error(request, 'Old password is incorrect.')
            else:
                request.user.set_password(form.cleaned_data['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('user_profile')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'users/change_password.html', {'form': form})


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def user_list(request):
    """List all users with search and filter"""
    users = UserProfile.objects.select_related('user', 'role').all()
    form = UserSearchForm(request.GET)
    
    if request.GET:
        search_query = request.GET.get('search')
        role_filter = request.GET.get('role')
        status_filter = request.GET.get('status')
        
        if search_query:
            users = users.filter(
                Q(user__username__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(department__icontains=search_query)
            )
        
        if role_filter:
            users = users.filter(role_id=role_filter)
        
        if status_filter:
            users = users.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(users, 10)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    
    context = {
        'users': users_page,
        'form': form,
        'total_users': paginator.count,
    }
    return render(request, 'users/user_list.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET"])
def user_detail(request, user_id):
    """View user details"""
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    assigned_tasks = user_profile.user.assigned_tasks.all()
    
    context = {
        'user_profile': user_profile,
        'assigned_tasks': assigned_tasks[:10],  # Recent tasks
    }
    return render(request, 'users/user_detail.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def create_user(request):
    """Create new user"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    context = {
        'form': form,
        'profile_form': profile_form,
        'title': 'Create User',
    }
    return render(request, 'users/create_user.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def edit_user(request, user_id):
    """Edit user details"""
    user = get_object_or_404(User, id=user_id)
    user_profile = user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'form': form,
        'user': user,
        'user_profile': user_profile,
        'title': f'Edit {user.get_full_name() or user.username}',
    }
    return render(request, 'users/edit_user.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["POST"])
def delete_user(request, user_id):
    """Delete user"""
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f'User {username} deleted successfully.')
    return redirect('user_list')


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET"])
def users_by_role(request, role_name):
    """View users by role"""
    role = get_object_or_404(Role, name=role_name)
    users = role.users.select_related('user').filter(status='active')
    
    paginator = Paginator(users, 10)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    
    context = {
        'role': role,
        'users': users_page,
        'total_users': paginator.count,
    }
    return render(request, 'users/users_by_role.html', context)
