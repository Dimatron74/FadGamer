# apps/admin_panel/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PromoCode, Service, BonusType
from .serializers import PromoCodeSerializer, ServiceSerializer, BonusTypeSerializer


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer

    @action(detail=False, methods=['get'])
    def services(self, request):
        """Получить список всех сервисов (игр)"""
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bonus_types(self, request):
        bonus_types = BonusType.objects.all()
        serializer = BonusTypeSerializer(bonus_types, many=True)
        return Response(serializer.data)