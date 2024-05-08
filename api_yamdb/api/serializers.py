from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('category',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'pub_date')    


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'pub_date')
