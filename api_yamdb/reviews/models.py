from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from reviews.validators import validate_year


User = get_user_model()
LENGTH_OF_NAME = 30
LENGTH_OF_REVIEW = 100
LENGTH_OF_COMMENT = 100


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'        
        ordering = ['name']
        default_related_name = 'category'

    def __str__(self):
        return self.name[:LENGTH_OF_NAME]


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'        
        ordering = ['name']
        default_related_name = 'genre'

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
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'        
        ordering = ('name',)
        default_related_name = 'titles'

    def __str__(self):
        return self.name[:LENGTH_OF_NAME]


class Comment(models.Model):
    text = models.TextField('Текст комментария',)
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
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий {self.author} на {self.review}'
    

class Review(models.Model):
    text = models.TextField('Текст отзыва',)
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE
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
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'reviews'
        unique_together = ('author', 'title')

    def __str__(self):
        return f'Отзыв {self.author} на "{self.title}"'
