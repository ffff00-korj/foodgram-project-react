from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    DownloadShoppingList,
    FavoriteRecipeCreateDelete,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingListCreateDelete,
    SubscriptionCreateDelete,
    SubscriptionList,
    TagViewSet,
)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


api = [
    path('recipes/download_shopping_cart/', DownloadShoppingList),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteRecipeCreateDelete.as_view(),
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingListCreateDelete.as_view(),
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionCreateDelete.as_view(),
    ),
    path(
        'users/subscriptions/',
        SubscriptionList.as_view(),
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('api/', include(api)),
]
