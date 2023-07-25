from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet)

api = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('api/', include(api)),
]
