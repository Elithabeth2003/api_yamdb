"""
Сериализаторы для взаимодействия с моделями в API.

Этот модуль содержит сериализаторы для взаимодействия с моделями,
такими как Category, Genre, Title, Comment и Review,
в рамках API Django REST Framework.

"""
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review
from reviews.models import User
from reviews.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        """Класс Meta."""

        model = Category
        fields = (
            'name',
            'slug'
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        """Класс Meta."""

        model = Genre
        fields = (
            'name',
            'slug'
        )


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о произведении (Title)."""

    genre = GenreSerializer(many=True,)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Класс Meta."""

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


class WriteTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о произведении (Title)."""

    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        """Класс Meta."""

        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title


class ReadCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о комментарии (Comment)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        """Класс Meta."""

        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = Comment


class WriteCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о комментарии (Comment)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        """Класс Meta."""

        fields = (
            'id',
            'text',
            'author',
        )
        model = Comment


class ReadReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о отзыве (Review)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        """Класс Meta."""

        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Review


class WriteReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о отзыве (Review)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        """Класс Meta."""

        fields = (
            'id',
            'text',
            'author',
            'score',
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
                'Отзыв на это произведение уже оставлен!')
        return data


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для административных операций с моделью User."""

    class Meta:
        """Класс Meta."""

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        """
        Проверяет правильность формата имени пользователя.

        Проверяет, соответствует ли имя пользователя заданному формату.
        """
        return validate_username(value)


class UserSerializer(AdminSerializer):
    """Сериализатор для базовых операций с моделью User."""

    username = serializers.SlugField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254,
    )
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        read_only=True
    )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate_username(self, value):
        """
        Проверяет правильность формата имени пользователя.

        Проверяет, соответствует ли имя пользователя заданному формату.
        """
        return validate_username(value)


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена аутентификации пользователя."""

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=255,
    )

    def validate_username(self, value):
        """
        Проверяет правильность формата имени пользователя.

        Проверяет, соответствует ли имя пользователя заданному формату.
        """
        return validate_username(value)
