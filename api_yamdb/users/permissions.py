"""Модуль permissions определяет пользовательские разрешения.

Этот модуль содержит класс UsersPermission, который определяет разрешение для
доступа к конечным точкам API только для аутентифицированных администраторов.
"""
from rest_framework.permissions import BasePermission


class UsersPermission(BasePermission):
    """UsersPermission.

    Проверяет, имеет ли пользователь
    право на доступ к конечной точке API.
    """

    def has_permission(self, request, view):
        """Определяет права доступа на уровне всего запроса."""
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
