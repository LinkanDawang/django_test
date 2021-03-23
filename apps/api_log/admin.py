from django.conf import settings
from django.contrib import admin

from .models import RequestLog


@admin.register(RequestLog)
class ApiDockingLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'requested_at'
    list_display = (
        'id',
        'requested_at',
        'response_ms',
        'status_code',
        "method",
        'device_model',
        'remote_addr',
        'ip_address'
    )
    list_filter = ("method", "status_code")
    search_fields = ('path',)
    raw_id_fields = ('user',)

    if getattr(settings, 'DRF_TRACKING_ADMIN_LOG_READONLY', False):
        readonly_fields = (
            'user',
            'username_persistent',
            'requested_at',
            'response_ms',
            'path',
            'view',
            'view_method',
            'remote_addr',
            'ip_address'
            'host',
            'method',
            'query_params',
            'data',
            'response',
            'errors',
            'status_code',
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_model_perms(self, request):
        return {
            'add': self.has_add_permission(request),
            'change': True,
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request),
        }
