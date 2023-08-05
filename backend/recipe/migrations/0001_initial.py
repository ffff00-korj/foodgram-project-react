# Generated by Django 3.2 on 2023-08-05 11:15

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'избранный рецепт',
                'verbose_name_plural': 'избранные рецепты',
                'default_related_name': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='название ингридиета', max_length=200, verbose_name='имя')),
                ('measurement_unit', models.CharField(help_text='единица изменения (например грамм)', max_length=200, verbose_name='ед. изм.')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': 'ингридиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='название рецепта', max_length=200, verbose_name='имя')),
                ('text', models.TextField(help_text='пошаговое описание процесса приготовления', verbose_name='описание')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='укажите время приготовления (в минутах)', validators=[django.core.validators.MinValueValidator(1, message='время приготовления должно быть больше 1ой минуты'), django.core.validators.MaxValueValidator(32767, message='время приготовления не должно превышать 32 767 минут')], verbose_name='время приготовления')),
                ('image', models.ImageField(blank=True, help_text='добавьте картинку к рецепту', upload_to='recipes/', verbose_name='картинка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='зарегистрированный пользователь, автор рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='название рецепта', max_length=200, verbose_name='имя')),
                ('slug', models.SlugField(help_text='идентификатор тэга', max_length=200, unique=True, verbose_name='слаг')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', help_text='цвет тега', image_field=None, max_length=7, samples=None, verbose_name='цвет')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(help_text='на кого подписался пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='subscribed', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('user', models.ForeignKey(help_text='пользователь, который подписался', on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='recipe.recipe', verbose_name='рецепты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'список покупок',
                'verbose_name_plural': 'списки покупок',
                'default_related_name': 'shopping_list',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngrideint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, help_text='количество ингридиентов для рецепта', validators=[django.core.validators.MinValueValidator(1, message='кол-во ингредиентов должно быть больше 1ой минуты'), django.core.validators.MaxValueValidator(32767, message='кол-во ингредиентов не должно превышать 32 767 минут')], verbose_name='количество ингридиентов')),
                ('ingredient', models.ForeignKey(help_text='ингредиет рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipe.ingredient', verbose_name='ингридиент')),
                ('recipe', models.ForeignKey(help_text='рецепт, к которому относится ингредиент', on_delete=django.db.models.deletion.CASCADE, related_name='ingrideints', to='recipe.recipe', verbose_name='рецепт')),
            ],
            options={
                'verbose_name': 'ингредиент рецепта',
                'verbose_name_plural': 'ингредиенты рецептов',
                'ordering': ('-amount',),
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, through='recipe.RecipeIngrideint', to='recipe.Ingredient', verbose_name='ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='метки, присвоенные рецепту', to='recipe.Tag', verbose_name='тег'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipe.recipe', verbose_name='рецепты'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_user_author'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='no_selt_sub'),
        ),
        migrations.AddConstraint(
            model_name='recipeingrideint',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
    ]
