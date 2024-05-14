"""
Конфигурация приложения Api.

Этот модуль содержит класс ApiConfig, который определяет
конфигурацию приложения Api.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Класс конфигурации приложения Api.

    Определяет конфигурацию для приложения Api, включая его имя.
    """

    name = 'api'
