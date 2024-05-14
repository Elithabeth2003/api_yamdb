"""Модуль serializers.

Определяет сериализаторы
для преобразования объектов моделей в JSON и обратно.
"""
import re

from rest_framework import serializers

from .models import User


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для административных операций с моделью User."""

    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False
    )

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
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Содержимое поля 'username' не "
                "соответствует паттерну ^[\\w.@+-]+\\Z$."
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для базовых операций с моделью User."""

    username = serializers.SlugField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254,
    )

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
        read_only_fields = (
            'username',
            'email',
            'role',
        )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    username = serializers.CharField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate_username(self, value):
        """
        Проверяет правильность формата имени пользователя.

        Проверяет, соответствует ли имя пользователя заданному формату.
        """
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Содержимое поля 'username' не "
                "соответствует паттерну ^[\\w.@+-]+\\Z$."
            )
        return value

    def validate(self, attrs):
        """
        Проверяет правильность введенных данных для регистрации.

        Проверяет, не используется ли имя 'me' в качестве имени пользователя.
        """
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено!"
            )
        return attrs


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена аутентификации пользователя."""

    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        max_length=255,
    )
