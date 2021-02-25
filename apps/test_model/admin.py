from django.contrib import admin
from django.conf import settings
from django.contrib import messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import Supplier, UploadFile


@admin.register(Supplier)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "fname", "create_time", "update_time", "state"]
    search_fields = ["name"]


class ProxyResource(resources.ModelResource):
    class Meta:
        model = UploadFile


@admin.register(UploadFile)
class FileAdmin(ImportExportActionModelAdmin):
    change_form_template = "upload.html"
    resource_class = ProxyResource
    list_display = ("id", "file", "file_temp", "file_icon", "create_time", "update_time")

    actions = ['custom_button', ]
    actions_on_top = False
    actions_on_bottom = True

    def custom_button(self, request, queryset):
        messages.add_message(request, messages.SUCCESS, '测试按钮点击成功')

    custom_button.enable = True
    custom_button.short_description = "按钮"
    # custom_button.icon = 'fas fa-audio-description'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'danger'
    # 给按钮追加自定义的颜色
    custom_button.style = 'color:black;'

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
    
    def save_model(self, request, obj, form, change):
        obj.file = obj.file_temp
        obj.save()
