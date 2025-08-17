# apps/games/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Game
from .serializers import GameSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# @method_decorator(cache_page(60 * 5), name='dispatch')
class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.filter(is_published=True).prefetch_related(
        'genres', 'platforms', 'acquisition_methods', 'acquisition_methods__service'
    )
    serializer_class = GameSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'