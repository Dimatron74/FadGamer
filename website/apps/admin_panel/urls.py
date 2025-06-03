# apps/admin_panel/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromoCodeViewSet, NewsCreateView, NewsEditView
from . import api

router = DefaultRouter()
router.register(r'promocodes', PromoCodeViewSet, basename='promocode')

urlpatterns = [
    path('', include(router.urls)),
    
    # Новости
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/<str:slug>/edit/', NewsEditView.as_view(), name='news-edit'),
    path('news/list/', api.get_news_list, name='news-list'),
    path('news/<str:slug>/delete/', api.delete_news, name='news-delete'),
]