"""
Конфигурация приложения Reviews.

Этот модуль содержит класс ReviewsConfig, который определяет конфигурацию приложения Reviews.
"""
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Класс конфигурации приложения Reviews.

    Определяет конфигурацию для приложения Reviews, включая его имя и отображаемое имя.
    """

    name = 'reviews'
    verbose_name = 'Отзывы'
