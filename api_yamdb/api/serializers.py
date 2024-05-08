from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title

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
