from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from gram.models import Tag

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='имя',
        help_text='название ингридиета',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='ед. изм.',
        help_text='единица изменения (например грамм)',
    )


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='имя',
        help_text='название рецепта',
    )
    text = models.TextField(
        verbose_name='описание',
        help_text='пошаговое описание процесса приготовления',
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='время приготовления',
        help_text='укажите время приготовления (в минутах)',
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
        help_text='зарегистрированный пользователь, автор рецепта',
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='recipes/',
        blank=True,
        help_text='добавьте картинку к рецепту',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='ингридиенты',
        blank=True,
        through='RecipeIngrideints',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тег',
        blank=True,
        help_text='метки, присвоенные рецепту',
    )


class RecipeIngrideints(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ингридиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество ингридиентов',
        help_text='количество ингридиентов для рецепта',
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        help_text='пользователь, владелец списка покупок',
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='рецепты',
        help_text='рецепты в списке покупок',
    )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        help_text='пользователь, который отметил рецепт',
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='рецепты',
        help_text='отмеченные рецепты',
    )
