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
    name = models.CharField(max_length=256, verbose_name='Название')
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
