from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import News
from .serializers import NewsSerializer

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True).prefetch_related('blocks')
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'