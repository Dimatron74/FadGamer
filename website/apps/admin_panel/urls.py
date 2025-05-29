# apps/admin_panel/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromoCodeViewSet

router = DefaultRouter()
router.register(r'promocodes', PromoCodeViewSet, basename='promocode')

urlpatterns = [
    path('', include(router.urls)),
]