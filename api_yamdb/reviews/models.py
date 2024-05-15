"""Модуль, определяющий модели для приложения отзывов."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import LENGTH_OF_NAME, MAX_VALUE, MIN_VALUE
from reviews.validators import validate_year

User = get_user_model()

class CategoryGenreBaseModel(models.Model):
    """Базовая модель для категорий и жанров произведений."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        """Возвращает строковое представление объекта категории."""
        return self.name[:LENGTH_OF_NAME]


class Category(CategoryGenreBaseModel):
    """Модель для категорий произведений."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']
        default_related_name = 'categories'


class Genre(CategoryGenreBaseModel):
    """Модель для жанров произведений."""

    class Meta:
        """Класс Meta."""

        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']
        default_related_name = 'genres'


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        max_length=256,
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
        """Класс Meta."""

        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('name',)
        default_related_name = 'titles'

    def __str__(self):
        """Возвращает строковое представление объекта произведения."""
        return self.name[:LENGTH_OF_NAME]


class CommentReviewBaseModel(models.Model):
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
        ordering = ['-pub_date']


class Comment(CommentReviewBaseModel):
    """Модель для комментариев к отзывам на произведения."""

    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        """Класс Meta."""

        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'

    def __str__(self):
        """Возвращает строковое представление объекта комментария."""
        return f'Комментарий {self.author} на {self.review}'


class Review(CommentReviewBaseModel):
    """Модель для отзывов на произведения."""

    score = models.IntegerField(
        'Оценка',
        validators=[MaxValueValidator(MAX_VALUE), MinValueValidator(MIN_VALUE)]
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        """Класс Meta."""

        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'reviews'
        unique_together = [['author', 'title']]

    def __str__(self):
        """Возвращает строковое представление объекта отзыва."""
        return f'Отзыв {self.author} на "{self.title}"'
