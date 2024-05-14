from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]


admin.site.register(User, UserAdmin)
