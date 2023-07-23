from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

from foodgram.utils import set_title_from_text

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='имя',
        help_text='название рецепта',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='идентификатор тэга',
    )
    color = ColorField(
        help_text='цвет тега',
    )

    def __str__(self) -> str:
        return set_title_from_text(self.name)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='user',
        on_delete=models.CASCADE,
        help_text='пользователь, который подписался',
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        related_name='author',
        on_delete=models.CASCADE,
        help_text='на кого подписался пользователь',
    )

    class Meta:
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
