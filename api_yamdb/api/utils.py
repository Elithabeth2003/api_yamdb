from random import sample
from django.core.mail import send_mail
from django.conf import settings

from api_yamdb.settings import (
    MAX_CONFIRMATION_CODE_ATTEMPTS,
    MAX_LENGTH_CONFIRMATION_CODE,
    VALID_CHARS_FOR_CONFIRMATION_CODE
)


def create_confirmation_code(user):
    """Создает код подтверждения."""
    user.confirmation_code = ''.join(
        sample(
            VALID_CHARS_FOR_CONFIRMATION_CODE,
            MAX_LENGTH_CONFIRMATION_CODE
        )
    )
    user.confirmation_code_attempts = MAX_CONFIRMATION_CODE_ATTEMPTS


def send_confirmation_code(user):
    """Отправляет код подтверждения на почту пользователя."""
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {user.confirmation_code}',
        settings.SENDER_EMAIL,
        [user.email]
    )
