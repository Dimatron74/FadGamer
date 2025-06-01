# apps/admin_panel/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PromoCode, Products, BonusType, UserPromoCodeActivation
from .serializers import PromoCodeSerializer, ServiceSerializer, BonusTypeSerializer
from django.shortcuts import get_object_or_404


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer

    @action(detail=False, methods=['get'])
    def services(self, request):
        """Получить список всех сервисов (игр)"""
        services = Products.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bonus_types(self, request):
        bonus_types = BonusType.objects.all()
        serializer = BonusTypeSerializer(bonus_types, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def activate(self, request):
        code = request.data.get('code')
        user = request.user

        if not code:
            return Response({'error': 'Не указан промокод'}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем промокод
        promo_code = PromoCode.objects.filter(code=code).first()

        # Промокод не найден
        if not promo_code:
            return Response({'error': 'Промокод не найден'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем статус промокода
        if not promo_code.status == 'active':
            return Response({'error': 'Этот промокод нельзя активировать'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что пользователь ещё не активировал этот промокод
        if UserPromoCodeActivation.objects.filter(user=user, promocode=promo_code).exists():
            return Response({'error': 'Вы уже активировали этот промокод'}, status=status.HTTP_400_BAD_REQUEST)

        # Увеличиваем счётчик активаций
        promo_code.activations_promo = promo_code.activations_promo + 1 if promo_code.activations_promo else 1
        promo_code.save()

        # Создаём запись об активации
        UserPromoCodeActivation.objects.create(user=user, promocode=promo_code)

        return Response({
            'success': f'Промокод "{promo_code.code}" успешно активирован!',
            'promocode_id': promo_code.id,
        }, status=status.HTTP_200_OK)