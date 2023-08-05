from colorfield.fields import ColorField
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


MAX_CHAR_LENGTH = 200
MAX_COLOR_LENGTH = 7


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        verbose_name='имя',
        help_text='название ингридиета',
    )
    measurement_unit = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        verbose_name='ед. изм.',
        help_text='единица изменения (например грамм)',
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit',
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        verbose_name='имя',
        help_text='название рецепта',
    )
    slug = models.SlugField(
        max_length=MAX_CHAR_LENGTH,
        unique=True,
        verbose_name='слаг',
        help_text='идентификатор тэга',
    )
    color = ColorField(
        max_length=MAX_COLOR_LENGTH,
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
        max_length=MAX_CHAR_LENGTH,
        verbose_name='имя',
        help_text='название рецепта',
    )
    text = models.TextField(
        verbose_name='описание',
        help_text='пошаговое описание процесса приготовления',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='время приготовления должно быть больше 1ой минуты'),
            MaxValueValidator(
            32767, message='время приготовления не должно превышать 32 767 минут')],
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
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.name


class RecipeIngrideint(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingrideints',
        verbose_name='рецепт',
        help_text='рецепт, к которому относится ингредиент',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        verbose_name='ингридиент',
        help_text='ингредиет рецепта',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='кол-во ингредиентов должно быть больше 1ой минуты'),
            MaxValueValidator(
            32767, message='кол-во ингредиентов не должно превышать 32 767 минут')],
        default=1,
        verbose_name='количество ингридиентов',
        help_text='количество ингридиентов для рецепта',
    )

    class Meta:
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты рецептов'
        ordering = ('-amount',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            ),
        ]

    def __str__(self):
        return f'{str(self.ingredient)} ({str(self.recipe)})'


class AbstractUserRecipeList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепты',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{str(self.recipe)} ({str(self.user)})'


class ShoppingList(AbstractUserRecipeList):

    class Meta:
        default_related_name = 'shopping_list'
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_shopping_list',
            ),
        ]


class FavoriteRecipe(AbstractUserRecipeList):

    class Meta:
        default_related_name = 'favorite'
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite',
            ),
        ]


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
        ordering = ('user',)
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

    def __str__(self):
        return f'{str(self.user)} ({str(self.author)})'
