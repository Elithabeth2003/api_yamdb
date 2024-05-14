"""Модуль, содержащий представления (viewsets) для работы с конечными точками API."""
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

from .permissions import AdminOrReadOnlyPermission


class BaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый класс для представлений (viewsets) с поддержкой операций списка, создания и удаления.

    Включает в себя функциональность списочного представления (ListModelMixin),
    представления создания объекта (CreateModelMixin) и представления удаления объекта (DestroyModelMixin).
    """

    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnlyPermission,)
