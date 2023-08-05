from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngrideint,
    ShoppingList,
    Subscription,
    Tag,
)


class RecipeIngrideintInline(admin.TabularInline):
    model = RecipeIngrideint
    extra = 1


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = ('name',)
    search_fields = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'cooking_time',
        'author',
        '_ingridients',
        '_tags',
    )
    list_editable = ('author', 'name')
    search_fields = ('author', 'name', '_tags')
    inlines = (RecipeIngrideintInline,)

    @admin.display(description='ингридиенты')
    def _ingridients(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]

    @admin.display(description='теги')
    def _tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_editable = ('slug',)
    search_fields = ('slug',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    list_editable = ('user', 'author')
    search_fields = ('user', 'author')
