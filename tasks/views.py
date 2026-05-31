from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import Task, TaskAssignment, TaskComment, TaskLog
from .forms import (
    TaskForm, TaskAssignmentForm, TaskCommentForm, 
    TaskFilterForm, TaskStatusUpdateForm
)
from users.rbac import admin_required, roles_required, user_owns_task

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def task_list(request):
    """List tasks based on user role"""
    user_profile = request.user.profile
    
    # Get appropriate task list based on role
    if user_profile.is_admin() or user_profile.is_manager():
        tasks = Task.objects.select_related('created_by', 'assigned_to').all()
    else:
        # Employees only see assigned tasks
        tasks = Task.objects.filter(assigned_to=request.user).select_related('created_by', 'assigned_to')
    
    form = TaskFilterForm(request.GET)
    
    if request.GET:
        search = request.GET.get('search')
        priority = request.GET.get('priority')
        status = request.GET.get('status')
        assigned_to = request.GET.get('assigned_to')
        due_date_from = request.GET.get('due_date_from')
        due_date_to = request.GET.get('due_date_to')
        
        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        if priority:
            tasks = tasks.filter(priority=priority)
        
        if status:
            tasks = tasks.filter(status=status)
        
        if assigned_to and (user_profile.is_admin() or user_profile.is_manager()):
            tasks = tasks.filter(assigned_to_id=assigned_to)
        
        if due_date_from:
            tasks = tasks.filter(due_date__gte=due_date_from)
        
        if due_date_to:
            tasks = tasks.filter(due_date__lte=due_date_to)
    
    # Order by priority and due date
    tasks = tasks.order_by('-priority', 'due_date')
    
    paginator = Paginator(tasks, 10)
    page = request.GET.get('page', 1)
    tasks_page = paginator.get_page(page)
    
    context = {
        'tasks': tasks_page,
        'form': form,
        'total_tasks': paginator.count,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def task_detail(request, task_id):
    """View task details"""
    task = get_object_or_404(Task, id=task_id)
    user_profile = request.user.profile
    
    # Check access permission
    can_view = (user_profile.is_admin() or 
                user_profile.is_manager() or
                task.assigned_to == request.user or 
                task.created_by == request.user)
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this task.')
        return redirect('task_list')
    
    comments = task.comments.select_related('author').all()
    logs = task.logs.select_related('performed_by').all()[:10]
    assignment_history = task.assignments.select_related('assigned_to', 'assigned_by').all()
    
    context = {
        'task': task,
        'comments': comments,
        'logs': logs,
        'assignment_history': assignment_history,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def create_task(request):
    """Create new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            
            # Log task creation
            TaskLog.objects.create(
                task=task,
                action='created',
                performed_by=request.user,
                description=f'Task created by {request.user.get_full_name() or request.user.username}'
            )
            
            # Create task assignment if assigned_to is provided
            if task.assigned_to:
                TaskAssignment.objects.create(
                    task=task,
                    assigned_to=task.assigned_to,
                    assigned_by=request.user,
                    notes=f'Initial assignment'
                )
                
                TaskLog.objects.create(
                    task=task,
                    action='assigned',
                    performed_by=request.user,
                    new_value=task.assigned_to.username,
                    description=f'Task assigned to {task.assigned_to.get_full_name() or task.assigned_to.username}'
                )
            
            messages.success(request, f'Task "{task.title}" created successfully.')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'title': 'Create Task',
    }
    return render(request, 'tasks/create_task.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def edit_task(request, task_id):
    """Edit task"""
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            
            # Log changes
            TaskLog.objects.create(
                task=task,
                action='status_changed',
                performed_by=request.user,
                description=f'Task updated'
            )
            
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'title': f'Edit: {task.title}',
    }
    return render(request, 'tasks/edit_task.html', context)


@login_required(login_url='login')
@admin_required
@require_http_methods(["POST"])
def delete_task(request, task_id):
    """Delete task"""
    task = get_object_or_404(Task, id=task_id)
    title = task.title
    task.delete()
    messages.success(request, f'Task "{title}" deleted successfully.')
    return redirect('task_list')


@login_required(login_url='login')
@admin_required
@require_http_methods(["GET", "POST"])
def assign_task(request, task_id):
    """Assign task to user"""
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            assigned_to = form.cleaned_data['assigned_to']
            notes = form.cleaned_data.get('notes', '')
            
            # Set previous assignment as not current
            TaskAssignment.objects.filter(task=task, is_current=True).update(is_current=False)
            
            # Create new assignment
            TaskAssignment.objects.create(
                task=task,
                assigned_to=assigned_to,
                assigned_by=request.user,
                notes=notes,
                is_current=True
            )
            
            # Update task
            task.assigned_to = assigned_to
            task.save()
            
            # Log assignment
            TaskLog.objects.create(
                task=task,
                action='reassigned' if task.assignments.count() > 1 else 'assigned',
                performed_by=request.user,
                new_value=assigned_to.username,
                description=f'Task assigned to {assigned_to.get_full_name() or assigned_to.username}'
            )
            
            messages.success(request, f'Task assigned to {assigned_to.get_full_name() or assigned_to.username}.')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskAssignmentForm()
    
    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'tasks/assign_task.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_task_status(request, task_id):
    """Update task status"""
    task = get_object_or_404(Task, id=task_id)
    user_profile = request.user.profile
    
    # Check access
    can_update = (user_profile.is_admin() or 
                  user_profile.is_manager() or
                  task.assigned_to == request.user)
    
    if not can_update:
        messages.error(request, 'You do not have permission to update this task.')
        return redirect('task_detail', task_id=task.id)
    
    form = TaskStatusUpdateForm(request.POST)
    if form.is_valid():
        old_status = task.get_status_display()
        task.status = form.cleaned_data['status']
        
        if task.status == 'completed':
            task.completed_date = timezone.now()
        
        task.save()
        
        # Log status change
        TaskLog.objects.create(
            task=task,
            action='status_changed',
            performed_by=request.user,
            old_value=old_status,
            new_value=task.get_status_display(),
            description=f'Status changed to {task.get_status_display()}'
        )
        
        if form.cleaned_data.get('notes'):
            TaskComment.objects.create(
                task=task,
                author=request.user,
                content=f"Status update: {form.cleaned_data['notes']}"
            )
        
        messages.success(request, f'Task status updated to {task.get_status_display()}.')
    
    return redirect('task_detail', task_id=task.id)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_comment(request, task_id):
    """Add comment to task"""
    task = get_object_or_404(Task, id=task_id)
    
    form = TaskCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.author = request.user
        comment.save()
        
        messages.success(request, 'Comment added successfully.')
    
    return redirect('task_detail', task_id=task.id)


@login_required(login_url='login')
@require_http_methods(["GET"])
def my_tasks(request):
    """View current user's assigned tasks"""
    tasks = request.user.assigned_tasks.select_related('created_by').all()
    
    # Filter options
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    tasks = tasks.order_by('-priority', 'due_date')
    
    paginator = Paginator(tasks, 10)
    page = request.GET.get('page', 1)
    tasks_page = paginator.get_page(page)
    
    # Calculate statistics
    stats = {
        'total': request.user.assigned_tasks.count(),
        'pending': request.user.assigned_tasks.filter(status='pending').count(),
        'in_progress': request.user.assigned_tasks.filter(status='in_progress').count(),
        'completed': request.user.assigned_tasks.filter(status='completed').count(),
    }
    
    context = {
        'tasks': tasks_page,
        'stats': stats,
    }
    return render(request, 'tasks/my_tasks.html', context)
