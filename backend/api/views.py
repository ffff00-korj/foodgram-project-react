from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
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
from rest_framework.decorators import action

from users.models import User
from api.filters import IngredientFilter, RecipeFilter
from api.pagination import PageLimitPagination
from api.serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingListSerializer,
    SubscriptionListSerializer,
    SubscriptionSerializer,
    TagSerializer,
)
from api.utils import shopping_cart_representation_response
from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngrideint,
    ShoppingList,
    Subscription,
    Tag,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    serializer_class = RecipeCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def add_shopping_cart(serializer_class, pk, request):
        shopping_cart = {'user': request.user.pk, 'recipe': pk}
        serializer = serializer_class(
            data=shopping_cart, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def add_favorite(serializer_class, pk, request):
        favorite = {'user': request.user.pk, 'recipe': pk}
        serializer = serializer_class(
            data=favorite, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk=None):
        return self.add_shopping_cart(ShoppingListSerializer, pk, request)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        get_object_or_404(ShoppingList, recipe=pk, user=request.user).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        return self.add_favorite(FavoriteRecipeSerializer, pk, request)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        get_object_or_404(
            FavoriteRecipe, recipe=pk, user=request.user
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        return shopping_cart_representation_response(
            RecipeIngrideint.objects.filter(
                recipe__shopping_list__user=request.user,
            )
            .select_related('recipes')
            .values(
                name=F('ingredient__name'),
                measurement_unit=F('ingredient__measurement_unit'),
            )
            .annotate(amount=Sum('amount'))
            .order_by('name')
        )


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


class SubscriptionCreateDelete(views.APIView):
    serializer_class = SubscriptionSerializer

    def post(self, request, user_id=None):
        subscription = {
            'user': request.user.pk,
            'author': user_id,
        }
        serializer = self.serializer_class(
            data=subscription, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, user_id=None):
        get_object_or_404(
            Subscription,
            author__pk=user_id,
            user=request.user,
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionList(generics.ListAPIView):
    pagination_class = PageLimitPagination
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return User.objects.filter(subscribed__user=self.request.user)
