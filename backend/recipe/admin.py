from django.contrib import admin
from django.utils.safestring import mark_safe
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
    min_num = 1


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
        '_image',
        '_ingridients',
        '_tags',
        '_favorite_count',
    )
    list_editable = ('author', 'name')
    search_fields = ('author', 'name', '_tags')
    inlines = (RecipeIngrideintInline,)

    @admin.display(description='ингридиенты')
    def _ingridients(self, recipe):
        return [ingredient.name for ingredient in recipe.ingredients.all()]

    @admin.display(description='теги')
    def _tags(self, recipe):
        return [tag.name for tag in recipe.tags.all()]

    @admin.display(description='В избранном')
    def _favorite_count(self, recipe):
        return recipe.favorite.count()

    @admin.display(description='картинка')
    def _image(self, recipe):
        return mark_safe(
            f'<img src={recipe.image.url} ' 'width="80" height="60">',
        )


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
