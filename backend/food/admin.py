from django.contrib import admin
from foodgram.admin import BaseAdmin
from food.models import Recipe, Ingredient, RecipeIngrideint, ShoppingList, FavoriteRecipe


class RecipeIngrideintInline(admin.TabularInline):
    model = RecipeIngrideint
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
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
        '_recipes',
    )
    list_editable = ('user',)
    search_fields = ('user',)

    @admin.display(description='рецепты')
    def _recipes(self, obj):
        return [recipes.name for recipes in obj.recipes.all()]


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        '_recipes',
    )
    list_editable = ('user',)
    search_fields = ('user',)

    @admin.display(description='рецепты')
    def _recipes(self, obj):
        return [recipes.name for recipes in obj.recipes.all()]
