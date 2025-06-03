# apps/games/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GamesViewSet

router = DefaultRouter()
router.register('', GamesViewSet, basename='games')

urlpatterns = [
    path('', include(router.urls)),
]