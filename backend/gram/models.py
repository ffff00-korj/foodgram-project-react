from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

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
        format='hexa',
        help_text='цвет тега',
    )


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
