"""
Модуль, определяющий модель пользователей приложения.

Этот модуль содержит определение пользовательской модели User, основанной
на абстрактной модели AbstractUser из Django.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.constants import LENGTH_OF_NAME


class User(AbstractUser):
    """Модель пользователя приложения."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150

    )
    email = models.EmailField(
        verbose_name='Email address',
        unique=True,
        max_length=254
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
        verbose_name='О себе',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        default='user',
        max_length=10,
        choices=ROLE_CHOICES
    )

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        """Проверяет, является ли пользователь обычным пользователем."""
        return self.role == self.USER

    def __str__(self):
        """Возвращает строковое представление объекта пользователя."""
        return self.username[:LENGTH_OF_NAME]
