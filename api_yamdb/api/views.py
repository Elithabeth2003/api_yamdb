from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS
from api.viewsets import BaseViewSet
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    ReadTitleSerializer,
    WriteTitleSerializer,
    CommentSerializer,
    ReadReviewSerializer,
    WriteReviewSerializer
)
from api.permissions import (AdminOrReadOnlyPermission,
                             AdminModeratorAuthorPermission)
from reviews.models import Category, Genre, Title, Review, Comment


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            rating=Avg('reviews__score')
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReadTitleSerializer
        return WriteTitleSerializer

    def perform_create(self, serializer):
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data.get('category')
            ),
            genre=Genre.objects.filter(
                slug__in=self.request.data.getlist('genre')
            )
        )

    def perform_update(self, serializer):
        self.perform_create(serializer)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def __get_review(self):
        return get_object_or_404(Comment, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.__get_review())

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.__get_review()
        )


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    #serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def __get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.__get_title())
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReadReviewSerializer
        return WriteReviewSerializer    

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.__get_title()
        )
