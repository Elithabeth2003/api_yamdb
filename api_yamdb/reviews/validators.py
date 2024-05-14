from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    if len(str(value)) != 4 or not isinstance(value, int):
        raise ValidationError("Дата введена неправильно, введите 4 цифры.")
    elif value > date.today().year:
        raise ValidationError("Год не может быть больше текущего.")
