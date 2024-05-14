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
    if len(str(value)) != 4 or not isinstance(value, int):
        raise ValidationError("Дата введена неправильно, введите 4 цифры.")
    elif value > date.today().year:
        raise ValidationError("Год не может быть больше текущего.")
