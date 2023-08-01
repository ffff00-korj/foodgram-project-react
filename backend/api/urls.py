from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    DownloadShoppingList,
    FavoriteRecipeCreateDelete,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingListCreateDelete,
    SubscriptionCreateDelete,
    SubscriptionViewSet,
    TagViewSet,
)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

subscriptions_router = DefaultRouter()
subscriptions_router.register('subscriptions', SubscriptionViewSet)

api = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/download_shopping_cart/', DownloadShoppingList),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingListCreateDelete.as_view(),
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteRecipeCreateDelete.as_view(),
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionCreateDelete.as_view(),
    ),
    path('users/', include(subscriptions_router.urls)),
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(api)),
]
