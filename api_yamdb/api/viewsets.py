from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

class BaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)