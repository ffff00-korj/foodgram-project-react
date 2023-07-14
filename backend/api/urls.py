from django.urls import include, path

api = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('api/', include(api)),
]
