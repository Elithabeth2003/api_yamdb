"""Модуль, определяющий модели для приложения отзывов."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from reviews.constants import LENGTH_OF_NAME
from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель для категорий произведений."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        """Класс Meta."""

        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']
        default_related_name = 'category'

    def __str__(self):
        """Возвращает строковое представление объекта категории."""
        return self.name[:LENGTH_OF_NAME]


class Genre(models.Model):
    """Модель для жанров произведений."""

    name = models.CharField(max_length=256, verbose_name='Название', )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        """Класс Meta."""

        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']
        default_related_name = 'genre'

    def __str__(self):
        """Возвращает строковое представление объекта жанра."""
        return self.name[:LENGTH_OF_NAME]


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


class Comment(models.Model):
    """Модель для комментариев к отзывам на произведения."""

    text = models.TextField('Текст комментария', )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )
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


class Review(models.Model):
    """Модель для отзывов на произведения."""

    text = models.TextField('Текст отзыва', )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        'Оценка',
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
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

    def __str__(self):
        """Возвращает строковое представление объекта отзыва."""
        return f'Отзыв {self.author} на "{self.title}"'

    def save(self, *args, **kwargs):
        """Переопределение метода save для проверки уникальности отзыва."""
        if self.pk is None:
            if Review.objects.filter(
                    author=self.author,
                    title=self.title
            ).exists():
                raise IntegrityError(
                    'Отзыв на это произведение уже оставлен!'
                )
        super().save(*args, **kwargs)
