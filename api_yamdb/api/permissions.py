"""Модуль permissions.

Определяет пользовательские разрешения
для доступа к конечным точкам API.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnlyPermission(BasePermission):
    """AdminOrReadOnlyPermission.

    Разрешение для доступа к конечным точкам API
    только для администраторов или в режиме "только чтение".
    Проверяет, имеет ли пользователь право на доступ к конечной точке API.
    """

    def has_permission(self, request, view):
        """Определяет права доступа на уровне всего запроса."""
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in SAFE_METHODS
                )


class AdminModeratorAuthorPermission(BasePermission):
    """AdminModeratorAuthorPermission.

    Разрешение для доступа к конечным точкам API администраторов,
    модераторов, авторов или в режиме "только чтение".

    Проверяет, имеет ли пользователь право на доступ к конечной точке API.
    Проверяет, имеет ли пользователь право на доступ к объекту.
    """

    def has_permission(self, request, view):
        """Определяет права доступа на уровне всего запроса."""
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        """Определяет, имеет ли пользователь разрешение на доступ к объекту."""
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                )


class IsAdminPermission(BasePermission):
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
