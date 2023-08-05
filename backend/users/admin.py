from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'username',
        'email',
        '_subscribers_count',
        '_recipes_count',
        'is_active',
        'is_superuser',
    )

    @admin.display(description='подписчиков')
    def _subscribers_count(self, user):
        return user.subscribed.count()

    @admin.display(description='рецептов')
    def _recipes_count(self, user):
        return user.recipes.count()


admin.site.unregister(auth_admin.Group)
