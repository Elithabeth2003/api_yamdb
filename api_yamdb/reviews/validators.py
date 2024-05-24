"""
Модуль, содержащий функции для валидации данных.

Этот модуль содержит функции для валидации данных,
используемые в приложении отзывов.
"""
import re
from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.deconstruct import deconstructible


def validate_year(value):
    """
    Проверка правильности введенного года.

    Функция проверяет, является ли значение года четырехзначным числом
    и не превышает ли оно текущий год.
    """
    if value > date.today().year:
        raise ValidationError(
            f'Введенный год {value} не может быть'
            f'больше текущего {date.today().year}.'
        )
    return value


@deconstructible
class ValidateUsername:
    def validate_username(self, username):
        """Проверка имени пользователя на соответствие шаблону."""
        if username == settings.USER_PROFILE_URL:
            raise ValidationError(
                (f'Использовать имя {settings.USER_PROFILE_URL} '
                 'в качестве username запрещено!')
            )
        matching_chars = ''.join(re.findall(r'[^\w.@+-]+', username))
        if matching_chars:
            raise ValidationError(
                f'Поле \'username\' содержит '
                f'недопустимые символы: {set(matching_chars)}'
            )
        return username

    def __call__(self, value):
        return self.validate_username(value)
