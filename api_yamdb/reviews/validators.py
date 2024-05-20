"""
Модуль, содержащий функции для валидации данных.

Этот модуль содержит функции для валидации данных,
используемые в приложении отзывов.
"""
from datetime import date
import re

from django.core.exceptions import ValidationError

from api_yamdb.constants import ME


def validate_year(value):
    """
    Проверка правильности введенного года.

    Функция проверяет, является ли значение года четырехзначным числом
    и не превышает ли оно текущий год.
    """
    if value > date.today().year:
        raise ValidationError(
            f'Введенный год ({value}) не может быть'
            f'больше текущего ({date.today().year}).'
        )
    return value


def validate_username(username):
    """Проверка имени пользователя на соответствие шаблону."""
    if username == ME:
        raise ValidationError(
            f'Использовать имя {ME} в качестве username запрещено!'
        )
    non_matching_chars = [char for char in username if not re.match(
        r'^[\w.@+-]+$', char
    )]
    if non_matching_chars:
        raise ValidationError(
            f'Содержимое поля \'username\' не '
            'соответствует паттерну ^[\\w.@+-]+\\Z$, '
            f'а именно содержит {non_matching_chars}'
        )
    return username
