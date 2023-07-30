from io import BytesIO
from typing import List, Union
from django.db.models import Sum

from django.db.models import QuerySet
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, response, status, viewsets

from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingListSerializer,
    TagSerializer,
)
from food.models import Ingredient, Recipe, RecipeIngrideint, ShoppingList
from foodgram.utils import base64_file
from gram.models import Tag


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        recipe = Recipe.objects.create(
            name=data['name'],
            cooking_time=data['cooking_time'],
            author=self.request.user,
            image=base64_file(data['image']),
            text=data['text'],
        )
        recipe.save()
        for ingredients in data['ingredients']:
            RecipeIngrideint.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, pk=ingredients['id']),
                amount=ingredients['amount'],
            ).save()

        for tag_id in data['tags']:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

        return response.Response(self.serializer_class(recipe).data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    pagination_class = None

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    pagination_class = None

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class ShoppingListCreateDelete(
    generics.CreateAPIView,
    generics.DestroyAPIView,
    generics.GenericAPIView,
):
    serializer_class = ShoppingListSerializer

    @cached_property
    def _recipe(self) -> Recipe:
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    def get_object(self):
        return get_object_or_404(
            ShoppingList,
            recipe=self._recipe,
            user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        if ShoppingList.objects.filter(
            user=request.user,
            recipe=self._recipe,
        ).exists():
            return response.Response(
                data={'detail': 'Рецепт уже в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingList.objects.create(
            user=request.user,
            recipe=self._recipe,
        ).save()
        return response.Response(status=status.HTTP_201_CREATED)

    def get_queryset(self) -> Union[QuerySet, List]:
        return self._recipe.shopping_list.all()


def DownloadShoppingList(request):
    ingredients = (
        RecipeIngrideint.objects.filter(
            recipe__in=request.user.shopping_list.values_list('recipe')
        )
        .values(
            'ingredient',
        )
        .annotate(Sum('amount'))
    )
    result = ''
    for row in ingredients:
        result += (
            f'* {row.get("ingredient__name")} '
            f'({row.get("ingredient__measurement_unit")}) '
            f'- {row.get("amount__sum")}\n'
        )

    return FileResponse(BytesIO(bytes(result, 'utf8')))
