from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

api = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('api/', include(api)),
]
