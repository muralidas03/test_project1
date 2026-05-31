from django.db import models

class Role(models.Model):
    """
    Role model for managing user roles in the system
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('team_lead', 'Team Lead'),
        ('employee', 'Employee'),
        ('guest', 'Guest'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True,
        choices=ROLE_CHOICES,
        help_text="Role name (must be unique)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the role and its responsibilities"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this role is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()
    
    def get_permissions(self):
        """Get all permissions associated with this role"""
        return self.permissions.filter(is_active=True)


class Permission(models.Model):
    """
    Permission model for role-based access control
    """
    PERMISSION_CHOICES = [
        # User Management
        ('view_user', 'View User'),
        ('add_user', 'Add User'),
        ('change_user', 'Change User'),
        ('delete_user', 'Delete User'),
        
        # Role Management
        ('view_role', 'View Role'),
        ('add_role', 'Add Role'),
        ('change_role', 'Change Role'),
        ('delete_role', 'Delete Role'),
        
        # Task Management
        ('view_task', 'View Task'),
        ('add_task', 'Add Task'),
        ('change_task', 'Change Task'),
        ('delete_task', 'Delete Task'),
        ('assign_task', 'Assign Task'),
        
        # Dashboard
        ('view_dashboard', 'View Dashboard'),
        ('view_reports', 'View Reports'),
        
        # Admin
        ('admin_access', 'Admin Access'),
    ]
    
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='permissions',
        help_text="Role this permission belongs to"
    )
    permission = models.CharField(
        max_length=100,
        choices=PERMISSION_CHOICES,
        help_text="Permission code"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of what this permission allows"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this permission is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        unique_together = ('role', 'permission')
        ordering = ['role', 'permission']
    
    def __str__(self):
        return f"{self.role.get_name_display()} - {self.get_permission_display()}"
