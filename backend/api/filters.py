import django_filters

from recipe.models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
