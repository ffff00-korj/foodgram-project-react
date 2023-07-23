from django.contrib import admin

from foodgram.admin import BaseAdmin
from gram.models import Tag


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'slug', 'color')
    list_editable = ('slug',)
    search_fields = ('slug',)
