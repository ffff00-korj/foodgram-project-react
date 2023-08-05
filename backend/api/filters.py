import django_filters

from recipe.models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='is_in_shopping_cart_filter',
    )
    is_favorited = django_filters.BooleanFilter(method='is_favorited_filter')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited')

    def is_in_shopping_cart_filter(self, queryset, value):
        return queryset.filter(
            pk__in=self.request.user.shopping_list.values('recipe'),
        )

    def is_favorited_filter(self, queryset, value):
        return queryset.filter(
            pk__in=self.request.user.favorite.values('recipe'),
        )


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
