from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "cell_phone", "is_superuser", "is_staff"]
    search_fields = ["username"]
