from django.db import models
from django.contrib.auth.models import User
from roles.models import Role

class UserProfile(models.Model):
    """
    Extended user profile with role and additional information
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Reference to Django User"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text="Assigned role for RBAC"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Department or team name"
    )
    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Job designation"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="User profile picture"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="User biography"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current user status"
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_login_tracked = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Last login time (custom tracking)"
    )
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        return self.user.email
    
    def get_role_display(self):
        """Get role display name"""
        return self.role.get_name_display() if self.role else "No Role"
    
    def has_permission(self, permission_code):
        """Check if user has specific permission"""
        if not self.role:
            return False
        return self.role.permissions.filter(
            permission=permission_code,
            is_active=True
        ).exists()
    
    def is_admin(self):
        return self.role and self.role.name == 'admin'
    
    def is_manager(self):
        return self.role and self.role.name == 'manager'
    
    def is_team_lead(self):
        return self.role and self.role.name == 'team_lead'
    
    def is_employee(self):
        return self.role and self.role.name == 'employee'
