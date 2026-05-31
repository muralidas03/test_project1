from django.contrib import admin
from .models import Task, TaskAssignment, TaskComment, TaskLog

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'assigned_to', 'due_date', 'created_at')
    list_filter = ('priority', 'status', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at', 'completed_date')
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description')
        }),
        ('Assignment & Status', {
            'fields': ('created_by', 'assigned_to', 'status', 'priority')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_date', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new task
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'assigned_to', 'assigned_by', 'assigned_date', 'is_current')
    list_filter = ('assigned_date', 'is_current')
    search_fields = ('task__title', 'assigned_to__username')
    readonly_fields = ('assigned_date', 'reassigned_date')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'action', 'performed_by', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('task__title', 'performed_by__username')
    readonly_fields = ('created_at',)
