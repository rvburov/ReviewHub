from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from rest_framework import validators

from .enums import UserRoles
from .models import User


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ!'
            ),
            validators.RegexValidator(
                regex=r'me',
                message='Использовать имя "me" запрещено!'
            ),
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Имя пользователя и Email должны отличаться!'
            )
        ]
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=UserRoles.choices(),
        default=UserRoles.user.name
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:50]

    @property
    def is_admin(self):
        return self.role == UserRoles.admin.name

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name

    @property
    def is_user(self):
        return self.role == UserRoles.user.name
