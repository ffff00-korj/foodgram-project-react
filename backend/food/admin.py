from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from food.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngrideint,
    ShoppingList,
)
from foodgram.admin import BaseAdmin


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
class RecipeAdmin(BaseAdmin):
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
class ShoppingListAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')
