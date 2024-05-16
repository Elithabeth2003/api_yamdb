"""Модуль, определяющий модели для приложения отзывов."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.utils import IntegrityError

from .constants import LENGTH_OF_NAME
from .validators import validate_year, validate_username


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
        max_length=150,
        validators=[validate_username]

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
    confirmation_code = models.CharField(
        max_length=4
    )

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

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

