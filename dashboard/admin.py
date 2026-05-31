from django.contrib import admin
from .models import DashboardCache

@admin.register(DashboardCache)
class DashboardCacheAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at', 'updated_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('key',)
    readonly_fields = ('created_at', 'updated_at')
