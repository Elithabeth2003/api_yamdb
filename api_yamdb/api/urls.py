from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

v1_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
