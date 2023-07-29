from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, response, viewsets

from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer,
)
from food.models import Ingredient, Recipe, RecipeIngrideint
from foodgram.utils import base64_file
from gram.models import Tag


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

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


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)

    pagination_class = None

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
