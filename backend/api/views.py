from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
