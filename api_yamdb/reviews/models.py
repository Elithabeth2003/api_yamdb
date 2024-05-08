from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year


LENGTH_OF_NAME = 30

class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name[:LENGTH_OF_NAME]


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name[:LENGTH_OF_NAME]


class Title(models.Model):
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
        verbose_name='Описание'
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'titles'

    def __str__(self):
        return self.name[:LENGTH_OF_NAME]


class Comment(models.Model):
    text = models.TextField('Текст комментария',)
    author = models.ForeignKey(
        'User',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )
    review = models.ForeignKey(
        'Review', 
        related_name='comments',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Комментарий {self.author} на {self.review}.'
    

class Review(models.Model):
    text = models.TextField('Текст отзыва',)
    author = models.ForeignKey(
        'User',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerChoices(
        'Оценка', 
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )
    title = models.ForeignKey(
        'Title',
        related_name='reviews',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return f'Отзыв {self.author} на {self.title__name}.'
