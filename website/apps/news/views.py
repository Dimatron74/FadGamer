#news/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import News
from .serializers import NewsSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5), name='dispatch')
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True).prefetch_related('blocks')
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'