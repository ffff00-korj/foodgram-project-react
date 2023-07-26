from rest_framework import permissions, viewsets, pagination
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from food.models import Ingredient, Recipe
from gram.models import Tag


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = pagination.PageNumberPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
