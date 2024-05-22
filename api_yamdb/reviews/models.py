"""Модуль, определяющий модели для приложения отзывов."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import MAX_LENGTH_CONFIRMATION_CODE
from api_yamdb.constants import (
    MAX_LENGTH_EMAIL_ADDRESS,
    MAX_LENGTH_FIRST_NAME,
    MAX_LENGTH_FOR_STR,
    MAX_LENGTH_LAST_NAME,
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    MAX_LENGTH_USERNAME,
    MAX_VALUE_SCORE,
    MIN_VALUE_SCORE,
    USER,
    MODERATOR,
    ADMIN,
    ROLE_CHOICES
)
from .validators import validate_year, ValidateUsername


class User(AbstractUser):
    """Модель пользователя приложения."""

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=[ValidateUsername()]

    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=MAX_LENGTH_EMAIL_ADDRESS
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH_FIRST_NAME,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH_LAST_NAME,
        blank=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        default=USER,
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES
    )
    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_CONFIRMATION_CODE
    )

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == MODERATOR

    @property
    def is_user(self):
        """Проверяет, является ли пользователь обычным пользователем."""
        return self.role == USER

    def __str__(self):
        """Возвращает строковое представление объекта пользователя."""
        return self.username[:MAX_LENGTH_FOR_STR]


class TypeNameBaseModel(models.Model):
    """Базовая модель для категорий и жанров произведений."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        """Возвращает строковое представление объекта категории."""
        return self.name[:MAX_LENGTH_FOR_STR]


class Category(TypeNameBaseModel):
    """Модель для категорий произведений."""

    class Meta(TypeNameBaseModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        default_related_name = 'categories'


class Genre(TypeNameBaseModel):
    """Модель для жанров произведений."""

    class Meta(TypeNameBaseModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        default_related_name = 'genres'


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название')
    year = models.IntegerField(
        verbose_name='Год',
        validators=[validate_year],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('name',)
        default_related_name = 'titles'

    def __str__(self):
        """Возвращает строковое представление объекта произведения."""
        return self.name[:MAX_LENGTH_FOR_STR]


class PublicationBaseModel(models.Model):
    """Базовая модель для комментариев и отзывов на произведения."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Comment(PublicationBaseModel):
    """Модель для комментариев к отзывам на произведения."""

    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(PublicationBaseModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'

    def __str__(self):
        """Возвращает строковое представление объекта комментария."""
        return f'Комментарий {self.author} на {self.review}'


class Review(PublicationBaseModel):
    """Модель для отзывов на произведения."""

    score = models.IntegerField(
        'Оценка',
        validators=[MaxValueValidator(MAX_VALUE_SCORE),
                    MinValueValidator(MIN_VALUE_SCORE)]
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta(PublicationBaseModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]

    def __str__(self):
        """Возвращает строковое представление объекта отзыва."""
        return f'Отзыв {self.author} на "{self.title}"'
