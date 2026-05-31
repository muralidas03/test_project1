from django.contrib import admin
from .models import Role, Permission

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Role Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('role__name', 'permission', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Permission Information', {
            'fields': ('role', 'permission', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
