from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
]

# добавил пока себе тоже, предлагаю отдельный файл для констант добавить
LENGTH_OF_NAME = 30


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150

    )
    email = models.EmailField(
        verbose_name='Email address',
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
        default=ROLE_CHOICES[0],
        max_length=10,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return self.username[:LENGTH_OF_NAME]

