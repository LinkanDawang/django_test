from django.contrib import admin
from django.conf import settings

from .models import Supplier, UploadFile


@admin.register(Supplier)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "fname", "create_time", "update_time", "state"]
    search_fields = ["name"]


@admin.register(UploadFile)
class FileAdmin(admin.ModelAdmin):
    change_form_template = "upload.html"
    list_display = ("id", "file", "create_time", "update_time")

    def set_extra_context(self, extra_context):
        oss_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        oss_access_key = settings.AWS_ACCESS_KEY_ID
        oss_secret_key = settings.AWS_SECRET_ACCESS_KEY
        oss_endpoint = settings.AWS_S3_ENDPOINT
        _extra_context = {
            "oss_bucket_name": oss_bucket_name,
            "oss_access_key": oss_access_key,
            "oss_secret_key": oss_secret_key,
            "oss_endpoint": oss_endpoint,
        }
        if extra_context and isinstance(extra_context, dict):
            extra_context.update(_extra_context)
        else:
            extra_context = _extra_context
        return extra_context

    def change_view(self, request, object_id, form_url='', extra_context=None):
        _extra_context = self.set_extra_context(extra_context)
        return super(FileAdmin, self).change_view(request, object_id, form_url, _extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        _extra_context = self.set_extra_context(extra_context)
        return super(FileAdmin, self).add_view(request, form_url, _extra_context)
