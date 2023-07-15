from django.contrib import admin

from foodgram.admin import BaseAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseAdmin):
    pass
