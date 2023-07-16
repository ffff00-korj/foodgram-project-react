from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
)
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer создания нового пользователя."""

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'password',
            'username',
        )


class UserCreateSerializer(DjoserUserCreateSerializer):
    """Serializer создания нового пользователя."""

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            'first_name',
            'last_name',
            'password',
            'username',
        )
