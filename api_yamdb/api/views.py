"""
Модуль, содержащий View для обработки запросов к API.

Этот модуль содержит классы View, предназначенных для обработки HTTP-запросов
к API для моделей Category, Genre, Title, Comment и Review.
Каждый класс View предоставляет функциональность для выполнения операций CRUD
(Create, Retrieve, Update, Delete) с соответствующей моделью.
"""
from random import sample

from django.conf import settings
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitleFilter
from api.permissions import (
    AdminModeratorAuthorPermission,
    AdminOrReadOnlyPermission,
    IsAdminPermission
)
from api.serializers import (
    AdminUserSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer,
    GetTokenSerializer, ReadTitleSerializer,
    ReviewSerializer, SignUpSerializer,
    UserSerializer, WriteTitleSerializer
)
from api.utils import send_confirmation_code
from api.viewsets import CRDSlugSearchViewSet
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategoryViewSet(CRDSlugSearchViewSet):
    """
    View для обработки запросов к модели Category.

    Позволяет выполнять операции CRUD с экземплярами модели Category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CRDSlugSearchViewSet):
    """
    View для обработки запросов к модели Genre.

    Позволяет выполнять операции CRUD с экземплярами модели Genre.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """
    View для обработки запросов к модели Title.

    Позволяет выполнять операции CRUD с экземплярами модели Title.
    Поддерживает фильтрацию, пагинацию и аннотации среднего рейтинга.
    """

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by(*Title._meta.ordering)
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """
        Получение класса сериализатора.

        Возвращает класс сериализатора в зависимости от метода запроса.
        """
        if self.request.method in SAFE_METHODS:
            return ReadTitleSerializer
        return WriteTitleSerializer


class CommentViewSet(ModelViewSet):
    """
    View для обработки запросов к модели Comment.

    Позволяет выполнять операции CRUD с экземплярами модели Comment.
    """

    queryset = Comment.objects.all()
    permission_classes = (AdminModeratorAuthorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = CommentSerializer

    def __get_review(self):
        """
        Получение отзыва по его идентификатору.

        Возвращает экземпляр модели Review по его идентификатору
        из параметров запроса.
        """
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        """
        Получение набора запросов для обработки.

        Возвращает набор запросов для обработки запросов к модели Comment.
        Фильтрует комментарии по отзыву, полученному из параметров запроса.
        """
        return self.__get_review().comments.all()

    def perform_create(self, serializer):
        """
        Выполнение создания комментария.

        Сохраняет комментарий, автором которого является текущий пользователь,
        и относящийся к отзыву полученному из параметров запроса.
        """
        serializer.save(
            author=self.request.user,
            review=self.__get_review()
        )


class ReviewViewSet(ModelViewSet):
    """
    View для обработки запросов к модели Review.

    Позволяет выполнять операции CRUD с экземплярами модели Review.
    """

    queryset = Review.objects.all()
    permission_classes = (AdminModeratorAuthorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = ReviewSerializer

    def __get_title(self):
        """
        Получение произведения по его идентификатору.

        Возвращает экземпляр модели Title по его идентификатору
        из параметров запроса.
        """
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        """
        Получение набора запросов для обработки.

        Возвращает набор запросов для обработки запросов к модели Review.
        Фильтрует отзывы по произведению, полученному из параметров запроса.
        """
        return self.__get_title().reviews.all()

    def perform_create(self, serializer):
        """
        Выполнение создания отзыва.

        Сохраняет отзыв, автором которого является текущий пользователь,
        относящийся к произведению полученному из параметров запроса.
        """
        serializer.save(
            author=self.request.user,
            title=self.__get_title()
        )


class UserViewSet(ModelViewSet):
    """Представление для операций с пользователями."""

    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        detail=False, methods=['GET', 'PATCH'],
        url_path=settings.USER_PROFILE_URL, url_name=settings.USER_PROFILE_URL,
        permission_classes=(IsAuthenticated,)
    )
    def profile(self, request):
        """Представление профиля текущего пользователя."""
        if not request.method == 'PATCH':
            return Response(
                UserSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    """Представление для регистрации новых пользователей."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Создает нового пользователя.

        Создает нового пользователя на основе введенных данных.
        Если пользователь уже существует, возвращает ошибку.
        Если email уже зарегистрирован, но с другим именем пользователя,
        возвращает данные этого пользователя.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        username = request.data.get('username')

        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            raise ValidationError(
                '{field} уже зарегистрирован!'.format(
                    field=username if User.objects.filter(
                        username=username
                    ).exists() else email
                )
            )

        user.confirmation_code = ''.join(
            sample(
                settings.VALID_CHARS_FOR_CONFIRMATION_CODE,
                settings.MAX_LENGTH_CONFIRMATION_CODE
            )
        )
        user.save()

        send_confirmation_code(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetTokenView(TokenObtainPairView):
    """Представление для получения токена аутентификации пользователя."""

    permission_classes = (AllowAny,)
    throttle_classes = (UserRateThrottle,)

    def post(self, request, *args, **kwargs):
        """
        Аутентифицирует пользователя и выдает токен аутентификации.

        Аутентифицирует пользователя по имени пользователя и
        коду подтверждения. Если аутентификация прошла успешно,
        выдает токен аутентификации.
        """
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if user.confirmation_code != request.data['confirmation_code']:
            raise ValidationError(
                'Неверный код подтверждения. Запросите код ещё раз.',
            )
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
