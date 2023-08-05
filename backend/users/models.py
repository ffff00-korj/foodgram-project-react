from django.contrib.auth.models import AbstractUser
from django.db import models

EMAIL_MAX_LENGTH = 254


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    email = models.EmailField(
        verbose_name='эл. почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        help_text='электронная почта пользователя',
    )
