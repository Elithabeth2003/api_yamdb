"""
Модуль, определяющий административные классы и ресурсы для административной панели Django.

Этот модуль содержит административные классы, используемые для отображения и управления моделями Django
в административной панели Django. Каждый административный класс связан с соответствующим ресурсом,
который используется для экспорта и импорта данных с использованием пакета import-export.
"""
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import DateTimeWidget, ForeignKeyWidget

from .models import Category, Comment, Genre, Title, Review


class CategoryResource(resources.ModelResource):
    """Ресурс для экспорта и импорта данных модели Category."""

    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
    """Административный класс для модели Category."""

    resource_classes = [CategoryResource]
    list_display = ('name', 'slug')
    search_fields = ('name',)


class GenreResource(resources.ModelResource):
    """Ресурс для экспорта и импорта данных модели Genre."""

    class Meta:
        model = Genre


class GenreAdmin(ImportExportModelAdmin):
    """Административный класс для модели Genre."""

    resource_classes = [GenreResource]
    list_display = ('name', 'slug')
    search_fields = ('name',)


class TitleResource(resources.ModelResource):
    """Ресурс для экспорта и импорта данных модели Title."""

    class Meta:
        model = Title


class TitleAdmin(ImportExportModelAdmin):
    """Административный класс для модели Title."""

    resource_classes = [TitleResource]
    list_display = ('name', 'year', 'category',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewResource(resources.ModelResource):
    """Ресурс для экспорта и импорта данных модели Review."""

    title = Field(column_name='title_id', attribute='title',
                  widget=ForeignKeyWidget(Title, 'pk', coerce_to_string=False))
    pub_date = Field(
        column_name='pub_date',
        attribute='pub_date',
        widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%S.%fZ')
    )

    class Meta:
        model = Review


class ReviewAdmin(ImportExportModelAdmin):
    """Административный класс для модели Review."""

    resource_classes = [ReviewResource]
    list_display = ('author', 'title', 'score', 'pub_date')
    search_fields = ('author', 'score',)


class CommentResource(resources.ModelResource):
    """Ресурс для экспорта и импорта данных модели Comment."""

    review = Field(column_name='review_id', attribute='review',
                   widget=ForeignKeyWidget(
                       Review, 'pk', coerce_to_string=False)
                   )
    pub_date = Field(
        column_name='pub_date',
        attribute='pub_date',
        widget=DateTimeWidget(format='%Y-%m-%dT%H:%M:%S.%fZ')
    )

    class Meta:
        model = Comment


class CommentAdmin(ImportExportModelAdmin):
    """Административный класс для модели Comment."""

    resource_classes = [CommentResource]
    list_display = ('author', 'pub_date', 'review',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
