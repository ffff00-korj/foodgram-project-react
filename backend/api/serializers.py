from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from recipe import constants
from recipe.models import (
    Ingredient,
    Recipe,
    RecipeIngrideint,
    ShoppingList,
    Subscription,
    Tag,
)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer получения пользователя."""

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

    def get_is_subscribed(self, author) -> bool:
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.subscriber.filter(author=author).exists()
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
        read_only = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.Serializer):
    """Ингридиенты рецептов и их количество."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=constants.MIN_VALUE_VALIDATION,
        max_value=constants.MAX_VALUE_VALIDATION,
    )

    class Meta:
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Ингридиенты рецептов и их количество."""

    class Meta:
        model = RecipeIngrideint
        fields = ('id', 'measurement_unit', 'name', 'amount')
        read_only = ('id', 'measurement_unit', 'name')


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer получения рецептов."""

    tags = TagSerializer(many=True)
    # ingredients = IngredientRecipeSerializer(
    #     source='ingrideints', many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

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
            'is_in_shopping_cart',
            'is_favorited',
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

    def get_is_favorited(self, recipe) -> bool:
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.favorite.filter(recipe=recipe).exists()
        )

    def get_is_in_shopping_cart(self, recipe) -> bool:
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.shopping_list.filter(recipe=recipe).exists()
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer получения рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(represent_in_base64=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cooking_time = serializers.IntegerField(
        min_value=constants.MIN_VALUE_VALIDATION,
        max_value=constants.MAX_VALUE_VALIDATION,
    )
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'author',
            'text',
            'tags',
            'ingredients',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        for ingredient_data in ingredients:
            RecipeIngrideint.objects.create(
                recipe=recipe,
                ingredient=ingredient_data.get('id'),
                amount=ingredient_data.get('amount'),
            ).save()

        for tag in tags:
            recipe.tags.add(tag)

        return recipe

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={"request": self.context.get("request")},
        ).data

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        RecipeIngrideint.objects.filter(recipe=recipe).delete()
        recipe.tags.set(validated_data.pop("tags"))
        ingredients = validated_data.pop("ingredients")
        for ingredient_data in ingredients:
            RecipeIngrideint.objects.create(
                recipe=recipe,
                ingredient=ingredient_data.get('id'),
                amount=ingredient_data.get('amount'),
            ).save()

        return super().update(recipe, validated_data)

    def validate(self, attrs):
        tags = attrs.get('tags')
        tags_len = len(tags)
        if not tags_len:
            raise serializers.ValidationError('Не выбрано ни одного тега.')
        if tags_len != len(set(tags)):
            raise serializers.ValidationError('Теги должны быть уникальны.')
        ingredients = [
            ingredient.get('id') for ingredient in attrs.get('ingredients')
        ]
        ingredients_len = len(ingredients)
        if not ingredients_len:
            raise serializers.ValidationError(
                'Не выбрано ни одного ингредиента.',
            )

        if ingredients_len != len(set(ingredients)):
            raise serializers.ValidationError(
                'Ингредиенты должны быть уникальны.',
            )
        return attrs


class ShoppingListSerializer(serializers.Serializer):
    class Meta:
        fields = (
            'user',
            'recipe',
        )
        validators = (
            validators.UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже есть в списке покупок',
            ),
        )


class FavoriteRecipeSerializer(serializers.Serializer):
    class Meta:
        fields = (
            'user',
            'recipe',
        )
        validators = (
            validators.UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже есть в избранном',
            ),
        )


class RecipeSubsriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email')
    id = serializers.EmailField(source='author.id')
    username = serializers.EmailField(source='author.username')
    first_name = serializers.EmailField(
        source='author.first_name',
        read_only=True,
    )
    last_name = serializers.EmailField(
        source='author.last_name',
        read_only=True,
    )
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'user',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.author.recipes
        request = self.context.get('request')
        if request:
            limit = request.query_params.get('recipes_limit')
            if limit:
                recipes = recipes[: int(limit)]
        return RecipeSubsriptionSerializer(recipes, many=True).data

    def get_is_subscribed(self, subscribtion) -> bool:
        return subscribtion.user.subscriber.filter(
            author=subscribtion.author,
        ).exists()
