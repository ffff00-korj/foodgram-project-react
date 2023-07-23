# Generated by Django 3.2 on 2023-07-22 15:34

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('gram', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='название ингридиета',
                        max_length=200,
                        verbose_name='имя',
                    ),
                ),
                (
                    'measurement_unit',
                    models.CharField(
                        help_text='единица изменения (например грамм)',
                        max_length=200,
                        verbose_name='ед. изм.',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='название рецепта',
                        max_length=200,
                        verbose_name='имя',
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        help_text='пошаговое описание процесса приготовления',
                        verbose_name='описание',
                    ),
                ),
                (
                    'cooking_time',
                    models.PositiveIntegerField(
                        help_text='укажите время приготовления (в минутах)',
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='время приготовления',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        blank=True,
                        help_text='добавьте картинку к рецепту',
                        upload_to='recipes/',
                        verbose_name='картинка',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        help_text='зарегистрированный пользователь, автор рецепта',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='автор',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'recipes',
                    models.ManyToManyField(
                        help_text='рецепты в списке покупок',
                        to='food.Recipe',
                        verbose_name='рецепты',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        help_text='пользователь, владелец списка покупок',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngrideints',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.PositiveIntegerField(
                        help_text='количество ингридиентов для рецепта',
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='количество ингридиентов',
                    ),
                ),
                (
                    'ingredient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='food.ingredient',
                        verbose_name='ингридиент',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='food.recipe',
                        verbose_name='рецепт',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                blank=True,
                through='food.RecipeIngrideints',
                to='food.Ingredient',
                verbose_name='ингридиенты',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                help_text='метки, присвоенные рецепту',
                to='gram.Tag',
                verbose_name='тег',
            ),
        ),
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'recipes',
                    models.ManyToManyField(
                        help_text='отмеченные рецепты',
                        to='food.Recipe',
                        verbose_name='рецепты',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        help_text='пользователь, который отметил рецепт',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
        ),
    ]
