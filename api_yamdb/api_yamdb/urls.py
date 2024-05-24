"""
URL-маршруты Django проекта.

Этот модуль определяет URL-маршруты для вашего Django приложения.
Он включает маршруты для административной панели, отображения документации API
и подключения URL-маршрутов из ваших приложений api и users.

"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls')),
]
