"""
Модуль URL определяет URL-шаблоны для конечных точек API для
аутентификации и управления пользователями.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, GetTokenView, UserViewSet


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet,
                   basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
]
