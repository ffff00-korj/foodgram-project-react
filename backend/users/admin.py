from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    empty_value_display = '-пусто-'
