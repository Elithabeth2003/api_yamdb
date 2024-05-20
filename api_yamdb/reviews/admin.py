"""Модуль, определяющий административные классы и ресурсы админ-панели.

Этот модуль содержит административные классы, используемые для отображения
и управления моделями Django в административной панели Django.
"""
from django.contrib import admin

from .models import Category, Comment, Genre, Title, Review, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административный класс для модели Category."""

    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административный класс для модели Genre."""

    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Административный класс для модели Title."""

    list_display = ('name', 'year', 'category',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административный класс для модели Review."""

    list_display = ('author', 'title', 'score', 'pub_date')
    search_fields = ('author', 'score',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административный класс для модели Comment."""

    list_display = ('author', 'pub_date', 'review')
    search_fields = ('author', 'review')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Административный класс для модели User."""

    list_display = ('username', 'role', 'email')
    search_fields = ('username', 'role')
