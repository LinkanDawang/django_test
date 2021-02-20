from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "fname", "create_time", "update_time", "state"]
    search_fields = ["name"]
