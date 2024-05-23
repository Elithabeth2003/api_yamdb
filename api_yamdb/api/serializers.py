"""
Сериализаторы для взаимодействия с моделями в API.

Этот модуль содержит сериализаторы для взаимодействия с моделями,
такими как Category, Genre, Title, Comment и Review,
в рамках API Django REST Framework.

"""
from django.core.exceptions import ValidationError
from rest_framework import serializers

from api_yamdb.settings import MAX_LENGTH_CONFIRMATION_CODE
from api_yamdb.constants import (
    MAX_LENGTH_EMAIL_ADDRESS,
    MAX_LENGTH_USERNAME,
    MAX_VALUE_SCORE,
    MIN_VALUE_SCORE,
)
from api_yamdb.constants import MAX_VALUE_SCORE, MIN_VALUE_SCORE
from reviews.models import Category, Genre, Title, Comment, Review, User
from reviews.validators import ValidateUsername, validate_year


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о произведении (Title)."""

    genre = GenreSerializer(many=True, )
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = fields


class WriteTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о произведении (Title)."""

    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

    def validate_year(self, value):
        """Проверяет, что год не превышает текущий год."""
        return validate_year(value)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и записи информации о комментарии (Comment)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и записи информации о отзыве (Review)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    score = serializers.IntegerField(
        min_value=MIN_VALUE_SCORE,
        max_value=MAX_VALUE_SCORE,
        error_messages={
            'min_value': f'Оценка должна быть не меньше {MIN_VALUE_SCORE}.',
            'max_value': f'Оценка должна быть не больше {MAX_VALUE_SCORE}.'
        }
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Review

    def validate(self, data):
        """
        Проверка валидности данных.

        Проверяет, что пользователь не оставляет
        повторные отзывы для одного произведения.
        """
        title_id = self.context.get('view').kwargs.get('title_id')
        if self.context['request'].method == 'POST' and Review.objects.filter(
            title=title_id, author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Отзыв на это произведение уже оставлен!'
            )
        return data


class AdminUserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Базовый сериализатор для операций с моделью User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserSerializer(AdminUserSerializer):
    """Сериализатор для базовых операций с моделью User."""

    class Meta(AdminUserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор для регистрации нового пользователя."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL_ADDRESS,
        required=True
    )


class GetTokenSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор для получения токена аутентификации пользователя."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=MAX_LENGTH_CONFIRMATION_CODE,
        required=True
    )
