from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_code(user):
    """Отправляет код подтверждения на почту пользователя."""
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {user.confirmation_code}',
        settings.SENDER_EMAIL,
        [user.email]
    )
