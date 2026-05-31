from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Task(models.Model):
    """
    Task model for managing tasks in the system
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(
        max_length=255,
        help_text="Task title/name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed task description"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Task priority level"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current task status"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
        help_text="User who created the task"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text="User assigned to this task"
    )
    due_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Task due date and time"
    )
    completed_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date and time when task was completed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['priority', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status != 'completed':
            return timezone.now() > self.due_date
        return False
    
    @property
    def days_remaining(self):
        """Calculate days remaining until due date"""
        if self.due_date:
            delta = self.due_date - timezone.now()
            return delta.days
        return None
    
    def mark_completed(self):
        """Mark task as completed"""
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.save()
    
    def get_assignment_history(self):
        """Get task assignment history"""
        return self.assignments.all().order_by('-assigned_date')


class TaskAssignment(models.Model):
    """
    Task assignment history to track who tasks were assigned to
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assignments',
        help_text="Reference to task"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='task_assignments',
        help_text="User the task is assigned to"
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_tasks_admin',
        help_text="User who assigned the task"
    )
    assigned_date = models.DateTimeField(auto_now_add=True)
    reassigned_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date when assignment was changed"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about assignment"
    )
    is_current = models.BooleanField(
        default=True,
        help_text="Whether this is the current assignment"
    )
    
    class Meta:
        db_table = 'task_assignments'
        verbose_name = 'Task Assignment'
        verbose_name_plural = 'Task Assignments'
        ordering = ['-assigned_date']
    
    def __str__(self):
        return f"{self.task.title} → {self.assigned_to.username}"


class TaskComment(models.Model):
    """
    Comments on tasks for communication and updates
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Reference to task"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='task_comments',
        help_text="User who added the comment"
    )
    content = models.TextField(help_text="Comment content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'task_comments'
        verbose_name = 'Task Comment'
        verbose_name_plural = 'Task Comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment on {self.task.title} by {self.author.username}"


class TaskLog(models.Model):
    """
    Activity log for task tracking and auditing
    """
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('assigned', 'Assigned'),
        ('reassigned', 'Reassigned'),
        ('status_changed', 'Status Changed'),
        ('priority_changed', 'Priority Changed'),
        ('completed', 'Completed'),
        ('commented', 'Commented'),
        ('deleted', 'Deleted'),
    ]
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='logs',
        help_text="Reference to task"
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        help_text="Action performed"
    )
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='task_logs',
        help_text="User who performed action"
    )
    old_value = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Old value before change"
    )
    new_value = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="New value after change"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of change"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task_logs'
        verbose_name = 'Task Log'
        verbose_name_plural = 'Task Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.task.title} - {self.get_action_display()}"
