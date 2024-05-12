from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet

from api.viewsets import BaseViewSet
from reviews.models import Category, Genre, Title, Review, Comment
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            rating=Avg('reviews__score')
        )
        return queryset

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
    serializer_class = ReviewSerializer

    def __get_title(self):
        return get_object_or_404(Review, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.__get_title())     

    def perform_create(self, serializer):
        serializer.save(
        author=self.request.user,
        title=self.__get_title()
        )