"""
Конфигурация приложения Users.

Этот модуль содержит класс UsersConfig, который определяет конфигурацию приложения Users.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Класс конфигурации приложения Users.

    Определяет конфигурацию для приложения Users, включая его имя.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
