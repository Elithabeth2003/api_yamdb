"""
Модуль, содержащий View для обработки запросов к API.

Этот модуль содержит классы View, предназначенных для обработки HTTP-запросов
к API для моделей Category, Genre, Title, Comment и Review.
Каждый класс View предоставляет функциональность для выполнения операций CRUD
(Create, Retrieve, Update, Delete) с соответствующей моделью.
"""
import random

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from api.viewsets import BaseViewSet
from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    ReadTitleSerializer,
    WriteTitleSerializer,
    ReadCommentSerializer,
    WriteCommentSerializer,
    ReadReviewSerializer,
    WriteReviewSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    UserSerializer,
    AdminSerializer
)
from api.permissions import (AdminOrReadOnlyPermission,
                             AdminModeratorAuthorPermission,
                             IsAdminPermission)
from reviews.models import Category, Genre, Title, Review, Comment, User
from reviews.constants import ME


class CategoryViewSet(BaseViewSet):
    """
    View для обработки запросов к модели Category.

    Позволяет выполнять операции CRUD с экземплярами модели Category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseViewSet):
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

    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        """
        Получение набора запросов для обработки.

        Возвращает набор запросов для обработки запросов к модели Title.
        Дополнительно аннотирует каждый объект рейтингом,
        вычисленным как среднее значение оценок из всех отзывов.
        """
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            rating=Avg('reviews__score')
        )
        return queryset

    def get_serializer_class(self):
        """
        Получение класса сериализатора.

        Возвращает класс сериализатора в зависимости от метода запроса.
        """
        if self.request.method in SAFE_METHODS:
            return ReadTitleSerializer
        return WriteTitleSerializer

    def perform_create(self, serializer):
        """
        Выполнение создания произведения.

        Сохраняет произведение, категорию и жанры из параметров запроса.
        """
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data.get('category')
            ),
            genre=Genre.objects.filter(
                slug__in=self.request.data.getlist('genre')
            )
        )

    def perform_update(self, serializer):
        """
        Выполнение обновления произведения.

        Повторяет действия perform_create для обновления произведения.
        """
        self.perform_create(serializer)


class CommentViewSet(ModelViewSet):
    """
    View для обработки запросов к модели Comment.

    Позволяет выполнять операции CRUD с экземплярами модели Comment.
    """

    queryset = Comment.objects.all()
    permission_classes = (AdminModeratorAuthorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def __get_review(self):
        """
        Получение отзыва по его идентификатору.

        Возвращает экземпляр модели Review по его идентификатору
        из параметров запроса.
        """
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """
        Получение набора запросов для обработки.

        Возвращает набор запросов для обработки запросов к модели Comment.
        Фильтрует комментарии по отзыву, полученному из параметров запроса.
        """
        return Comment.objects.filter(review=self.__get_review())

    def get_serializer_class(self):
        """
        Получение класса сериализатора.

        Возвращает класс сериализатора в зависимости от метода запроса.
        """
        if self.request.method in SAFE_METHODS:
            return ReadCommentSerializer
        return WriteCommentSerializer

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

    def __get_title(self):
        """
        Получение произведения по его идентификатору.

        Возвращает экземпляр модели Title по его идентификатору
        из параметров запроса.
        """
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """
        Получение набора запросов для обработки.

        Возвращает набор запросов для обработки запросов к модели Review.
        Фильтрует отзывы по произведению, полученному из параметров запроса.
        """
        return Review.objects.filter(title=self.__get_title())

    def get_serializer_class(self):
        """
        Получение класса сериализатора.

        Возвращает класс сериализатора в зависимости от метода запроса.
        """
        if self.request.method in SAFE_METHODS:
            return ReadReviewSerializer
        return WriteReviewSerializer

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
    serializer_class = AdminSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        detail=False, methods=['GET', 'PATCH'],
        url_path=f'{ME}', url_name=f'{ME}',
        permission_classes=(IsAuthenticated,)
    )
    def profile(self, request):
        """Представление профиля текущего пользователя."""
        if not request.method == 'PATCH':
            serializer = UserSerializer(
                request.user
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
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
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
            if created:
                confirmation_code = ''.join(
                    str(random.randint(0, 9)) for _ in range(4)
                )
                user.confirmation_code = confirmation_code
                user.save()

            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {user.confirmation_code}',
                settings.SENDER_EMAIL,
                [email]
            )
            
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except IntegrityError as error:
            if 'email' in error.args[0]:
                return Response(
                    {'error': 'Email уже зарегистрирован!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'username' in error.args[0]:
                return Response(
                    {'error': 'Пользователь с таким именем уже '
                              'зарегистрирован!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {'error': 'Произошла ошибка: {error.args[0]}'},
                    status=status.HTTP_400_BAD_REQUEST
                )


class GetTokenView(TokenObtainPairView):
    """Представление для получения токена аутентификации пользователя."""

    permission_classes = (AllowAny,)

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
                'Неверный код подтверждения!',
            )
        token = {'token': str(AccessToken.for_user(user))}
        return Response(
            token,
            status=status.HTTP_200_OK
        )
