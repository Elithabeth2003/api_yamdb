import re

from rest_framework import serializers

from .models import User


class AdminSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False
    )

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

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Содержимое поля 'username' не "
                "соответствует паттерну ^[\\w.@+-]+\\Z$."
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254,
    )

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
        read_only_fields = (
            'username',
            'email',
            'role',
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Содержимое поля 'username' не "
                "соответствует паттерну ^[\\w.@+-]+\\Z$."
            )
        return value

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено!"
            )
        return attrs


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        max_length=255,
    )
