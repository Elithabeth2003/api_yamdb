"""
Модуль, определяющий административные классы и ресурсы для административной панели Django.

Этот модуль содержит административные классы и ресурсы, используемые для отображения и управления моделей Django
в административной панели Django. Он также использует пакет import-export для экспорта и импорта данных.
"""
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import User


class UserResource(resources.ModelResource):
    """Ресурс для экспорта и импорта данных модели User."""

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    """Административный класс для модели User."""

    resource_classes = [UserResource]


admin.site.register(User, UserAdmin)
