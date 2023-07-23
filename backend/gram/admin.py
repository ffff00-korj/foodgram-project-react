from django.contrib import admin

from foodgram.admin import BaseAdmin
from gram.models import Tag, Subscription


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'slug', 'color')
    list_editable = ('slug',)
    search_fields = ('slug',)


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    list_editable = ('user', 'author')
    search_fields = ('user', 'author')
