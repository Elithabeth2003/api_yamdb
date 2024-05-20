"""
Модуль, содержащий функции для валидации данных.

Этот модуль содержит функции для валидации данных,
используемые в приложении отзывов.
"""
from datetime import date
import re

from django.core.exceptions import ValidationError

from api_yamdb.constants import MAX_VALUE_SCORE, MIN_VALUE_SCORE, ME


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


class ValidateUsername:
    def validate_username(self, username):
        """Проверка имени пользователя на соответствие шаблону."""
        if username == ME:
            raise ValidationError(
                f'Использовать имя {ME} в качестве username запрещено!'
            )
        matching_chars = re.findall(r'^[\w.@+-]+$', username)
        if not matching_chars:
            raise ValidationError(
                f'Содержимое поля \'username\' недопустимые символы, '
                f'а именно содержит {matching_chars}'
            )
        return username

    def __call__(self, value):
        return self.validate_username(value)


def validate_score(score):
    """Проверка соответствия оценки произведения заданным границам."""
    if score not in range(MIN_VALUE_SCORE, MAX_VALUE_SCORE + 1):
        raise ValidationError(
            'Оценка произведения должны быть в пределах '
            f'от {MIN_VALUE_SCORE} до {MAX_VALUE_SCORE}.'
        )
    return score
