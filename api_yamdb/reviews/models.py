from django.db import models


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
    year = models.IntegerField(verbose_name='Год', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        ordering = ['name']
        default_related_name = 'titles'

    def __str__(self):
        return self.name[:LENGTH_OF_NAME]
