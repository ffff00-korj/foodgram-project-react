from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db.models import F

from food.models import Ingredient, Recipe, RecipeIngrideint
from gram.models import Tag

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    """Serializer получения пользователя."""

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )
    email = serializers.EmailField(required=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'password',
            'username',
            'is_subscribed',
        )

    def get_is_subscribed(self, user: User) -> bool:
        return (
            self.context.get('request')
            .user.subscriber.filter(author=user)
            .exists()
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer получения рецептов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer получения рецептов"""

    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    author = UserSerializer()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'author',
            'id',
            'name',
            'image',
            'text',
            'tags',
            'ingredients',
            'cooking_time',
        )
