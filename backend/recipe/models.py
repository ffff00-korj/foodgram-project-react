from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

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

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='имя',
        help_text='название рецепта',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='слаг',
        help_text='идентификатор тэга',
    )
    color = ColorField(
        verbose_name='цвет',
        help_text='цвет тега',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['slug']

    def __str__(self) -> str:
        return self.name


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
        related_name='recipes',
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
        through='RecipeIngrideint',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тег',
        blank=True,
        help_text='метки, присвоенные рецепту',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class RecipeIngrideint(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingrideints',
        verbose_name='рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        verbose_name='ингридиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name='количество ингридиентов',
        help_text='количество ингридиентов для рецепта',
    )

    class Meta:
        ordering = ['-amount']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            ),
        ]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        help_text='пользователь, владелец списка покупок',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепты',
        on_delete=models.CASCADE,
        help_text='рецепты в списке покупок',
    )

    class Meta:
        default_related_name = 'shopping_list'
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe',
            ),
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        help_text='пользователь, который отметил рецепт',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепты',
        on_delete=models.CASCADE,
        help_text='отмеченные рецепты',
    )

    class Meta:
        default_related_name = 'favorite'
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='subscriber',
        on_delete=models.CASCADE,
        help_text='пользователь, который подписался',
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        related_name='subscribed',
        on_delete=models.CASCADE,
        help_text='на кого подписался пользователь',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_selt_sub',
            ),
        ]
