"""Модуль filters определяет фильтры для конечной точки API, связанной с моделью Title."""
from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для модели Title, используемый в конечной точке API."""

    name = CharFilter(lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        """Класс Meta."""

        model = Title
        fields = ['year']
