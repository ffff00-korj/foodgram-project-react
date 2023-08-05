from io import BytesIO
from typing import List, Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    generics,
    permissions,
    response,
    status,
    views,
    viewsets,
)
from rest_framework.decorators import api_view

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import PageLimitPagination
from api.serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    RecipeSubsriptionSerializer,
    ShoppingListSerializer,
    SubscriptionSerializer,
    TagSerializer,
)
from foodgram.utils import base64_file
from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngrideint,
    ShoppingList,
    Subscription,
    Tag,
)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination

    serializer_class = RecipeCreateSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = ('author', 'tags')

    def get_queryset(self):
        query_params = self.request.query_params
        if query_params.get('is_in_shopping_cart'):
            return self.queryset.filter(
                id__in=self.request.user.shopping_list.values('recipe'),
            )
        if query_params.get('is_favorited'):
            return self.queryset.filter(
                id__in=self.request.user.favorite.values('recipe'),
            )
        return self.queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        recipe = Recipe.objects.create(
            name=data['name'],
            cooking_time=data['cooking_time'],
            author=request.user,
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

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    permission_classes = (permissions.AllowAny,)

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = IngredientFilter
    filterset_fields = ('name',)
    ordering_fields = ('name',)


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
                data={'errors': 'Рецепт уже в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shopping_list = ShoppingList.objects.create(
            user=request.user,
            recipe=self._recipe,
        )
        shopping_list.save()
        serializer = RecipeSubsriptionSerializer(shopping_list.recipe)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self) -> Union[QuerySet, List]:
        return self._recipe.shopping_list.all()


@api_view(['GET'])
def DownloadShoppingList(request):
    ingredients = (
        RecipeIngrideint.objects.filter(
            recipe__in=request.user.shopping_list.values_list('recipe'),
        )
        .select_related('recipes')
        .values(
            'ingredient__name',
            'ingredient__measurement_unit',
        )
        .annotate(amount=Sum('amount'))
    )
    result = ''
    for row in ingredients:
        result += (
            f'* {row.get("ingredient__name")} '
            f'({row.get("ingredient__measurement_unit")}) '
            f'- {row.get("amount")}\n'
        )

    return FileResponse(BytesIO(bytes(result, 'utf8')))


class FavoriteRecipeCreateDelete(
    generics.CreateAPIView,
    generics.DestroyAPIView,
    generics.GenericAPIView,
):
    serializer_class = FavoriteRecipeSerializer

    @cached_property
    def _recipe(self) -> Recipe:
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    def get_object(self):
        return get_object_or_404(
            FavoriteRecipe,
            recipe=self._recipe,
            user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        if FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=self._recipe,
        ).exists():
            return response.Response(
                data={'errors': 'Рецепт уже в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite = FavoriteRecipe.objects.create(
            user=request.user,
            recipe=self._recipe,
        )
        favorite.save()
        serializer = RecipeSubsriptionSerializer(favorite.recipe)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self) -> Union[QuerySet, List]:
        return self._recipe.shopping_list.all()


class SubscriptionCreateDelete(views.APIView):
    serializer_class = SubscriptionSerializer

    @cached_property
    def _author(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_object(self):
        return get_object_or_404(
            Subscription,
            author=self._author,
            user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        if Subscription.objects.filter(
            user=request.user,
            author=self._author,
        ).exists():
            return response.Response(
                data={'errors': 'Вы уже подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = Subscription.objects.create(
            user=request.user,
            author=self._author,
        )
        subscription.save()
        serializer = self.serializer_class(subscription)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self) -> Union[QuerySet, List]:
        return self._recipe.shopping_list.all()


class SubscriptionList(generics.ListAPIView):
    queryset = Subscription.objects.all()
    pagination_class = PageLimitPagination
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscriber.all()
