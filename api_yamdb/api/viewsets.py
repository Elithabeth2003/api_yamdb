from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

from .permissions import AdminOrReadOnlyPermission


class BaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnlyPermission,)
