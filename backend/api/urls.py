from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    DownloadShoppingList,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingListCreateDelete,
    FavoriteRecipeCreateDelete,
    TagViewSet,
)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

api = [
    path('recipes/download_shopping_cart/', DownloadShoppingList),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingListCreateDelete.as_view(),
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteRecipeCreateDelete.as_view(),
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]

urlpatterns = [
    path('api/', include(api)),
]
