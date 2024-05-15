"""
Модуль, содержащий функции для валидации данных.

Этот модуль содержит функции для валидации данных,
используемые в приложении отзывов.
"""
from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Проверка правильности введенного года.

    Функция проверяет, является ли значение года четырехзначным числом
    и не превышает ли оно текущий год.
    """
    if value > date.today().year:
        raise ValidationError(
            f"""Введенный год ({value})
            не может быть больше текущего ({date.today().year})."""
        )
    return value
