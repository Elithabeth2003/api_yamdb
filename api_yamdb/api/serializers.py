from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class ReadTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
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


class WriteTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True,
        slug_field='slug', queryset = Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset = Category.objects.all()
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


class CommentSerializer(serializers.ModelSerializer):
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
        read_only_fields = (
            'id', 
            'pub_date'
        )    


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
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
        read_only_fields = (
            'id', 
            'pub_date'
        )
