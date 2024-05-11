from django.contrib import admin

from .models import Category, Comment, Genre, Title, Review

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category

class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name', 'slug')
    search_fields = ('name',)


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre

class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = ('name', 'slug')
    search_fields = ('name',)


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title

class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = ('name', 'year', 'category',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewResource(resources.ModelResource):

    class Meta:
        model = Review

class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]
    list_display = ('author', 'title', 'score', 'pub_date')
    search_fields = ('author','score',)


class CommentResource(resources.ModelResource):

    class Meta:
        model = Comment

class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]
    list_display = ('author', 'pub_date', 'review',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
