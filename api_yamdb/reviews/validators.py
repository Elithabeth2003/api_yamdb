from django.core.exceptions import ValidationError


def validate_year(value):
    if len(str(value)) != 4 or not value.isdigit():
        raise ValidationError("Дата введена неправильно, введите 4 цифры.")
