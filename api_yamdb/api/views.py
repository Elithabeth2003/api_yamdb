from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, mixins

from reviews.models import Category, Genre, Title, Review, Comment
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('rating')
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination

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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
