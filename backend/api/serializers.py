from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from food.models import Ingredient, Recipe, RecipeIngrideint, ShoppingList
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
    """Serializer получения рецептов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.Serializer):
    """Ингридиенты рецептов и их количество."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer получения рецептов."""

    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
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

    def get_ingredients(self, recipe):
        result = []
        for row in RecipeIngrideint.objects.filter(
            recipe=recipe,
        ).select_related('ingredient'):
            result.append(
                {
                    'id': row.ingredient.pk,
                    'name': row.ingredient.name,
                    'measurement_unit': row.ingredient.measurement_unit,
                    'amount': row.amount,
                },
            )
        return result


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer получения рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'text',
            'tags',
            'ingredients',
            'cooking_time',
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingListSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), required=False
    )
    validators = (
        validators.UniqueTogetherValidator(
            queryset=ShoppingList.objects.all(),
            fields=('user', 'recipe'),
            message='Этот рецепт уже есть в списке покупок',
        ),
    )

    class Meta:
        fields = (
            'user',
            'recipe',
        )


class FavoriteRecipeSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), required=False
    )
    validators = (
        validators.UniqueTogetherValidator(
            queryset=ShoppingList.objects.all(),
            fields=('user', 'recipe'),
            message='Этот рецепт уже есть в избранном',
        ),
    )

    class Meta:
        fields = (
            'user',
            'recipe',
        )
