# Generated by Django 3.2 on 2023-08-05 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipe', '0002_auto_20230805_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingrideint',
            name='amount',
            field=models.PositiveIntegerField(
                default=1,
                help_text='количество ингридиентов для рецепта',
                validators=[
                    django.core.validators.MinValueValidator(
                        1,
                        message='кол-во ингредиентов должно быть больше одного',
                    ),
                    django.core.validators.MaxValueValidator(
                        32767,
                        message='кол-во ингредиентов не должно превышать 32 767 ед.',
                    ),
                ],
                verbose_name='количество ингридиентов',
            ),
        ),
    ]
