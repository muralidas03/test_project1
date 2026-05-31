from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'status', 'date_joined')
    list_filter = ('role', 'status', 'date_joined')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'department')
    readonly_fields = ('date_joined', 'last_modified', 'user')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone', 'email_display')
        }),
        ('Role & Status', {
            'fields': ('role', 'status')
        }),
        ('Organization', {
            'fields': ('department', 'designation')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'bio'),
            'classes': ('collapse',)
        }),
        ('Activity', {
            'fields': ('last_login_tracked', 'date_joined', 'last_modified'),
            'classes': ('collapse',)
        }),
    )
    
    def email_display(self, obj):
        return obj.email
    email_display.short_description = 'Email'
    
    readonly_fields = ('date_joined', 'last_modified', 'user', 'email_display')
