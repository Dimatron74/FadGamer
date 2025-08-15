# admin_panel/api.py

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ..news.serializers import NewsSerializer
from ..news.models import News
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserPromoCodeActivation


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])
def create_news(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_news(request, slug):
    try:
        news = News.objects.get(slug=slug)
    except News.DoesNotExist:
        return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsSerializer(news, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_news_list(request):
    try:
        news = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(news, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])
def delete_news(request, slug):
    try:
        news = News.objects.get(slug=slug)
        news.delete()
        return Response({'success': 'Новость успешно удалена'})
    except News.DoesNotExist:
        return Response({'error': 'Новость не найдена'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)



# Промокоды

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from .models import PromoCode, UserPromoCodeActivation
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_unclaimed_promocodes(request):
    user = request.user
    # Получаем все активированные, но неприменённые промокоды
    activations = UserPromoCodeActivation.objects.filter(
        user=user,
        is_applied=False
    ).select_related('promocode')
    
    if not activations.exists():
        return Response([], status=status.HTTP_200_OK)

    result = [{
        'id': act.promocode.id,
        'code': act.promocode.code,
        'bonuses': [{
            'type': bonus.bonus_type.code,
            'amount': bonus.amount
        } for bonus in act.promocode.bonuses.all()]
    } for act in activations]

    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def activate_promocode(request):
    """
    Пользователь активирует промокод.
    """
    code = request.data.get('code', '').strip()

    if not code:
        return Response(
            {'error': 'Не указан промокод.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user

    # Ищем промокод по коду (без учёта регистра)
    promo_code = get_object_or_404(PromoCode, code__iexact=code)

    # Проверяем, активен ли промокод
    if promo_code.status != 'active':
        return Response(
            {'error': 'Этот промокод неактивен.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Проверяем, не исчерпано ли количество активаций
    if promo_code.max_activations and promo_code.activations_promo >= promo_code.max_activations:
        return Response(
            {'error': 'Лимит активаций этого промокода исчерпан.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Проверяем, не активировал ли пользователь этот промокод ранее
    if UserPromoCodeActivation.objects.filter(user=user, promocode=promo_code).exists():
        return Response(
            {'error': 'Вы уже активировали этот промокод.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Увеличиваем счётчик активаций
    promo_code.activations_promo = (promo_code.activations_promo or 0) + 1
    promo_code.save()

    # Создаём запись об активации
    activation = UserPromoCodeActivation.objects.create(
        user=user,
        promocode=promo_code,
        is_applied=False  # бонусы ещё не начислены
    )

    # Возвращаем информацию о бонусах
    bonuses = [
        {
            'type': bonus.bonus_type.code,
            'amount': bonus.amount,
            'description': bonus.bonus_type.description
        }
        for bonus in promo_code.bonuses.all()
    ]

    return Response({
        'success': True,
        'message': f'Промокод "{promo_code.code}" успешно активирован!',
        'activation_id': activation.id,
        'bonuses': bonuses,
        'promocode_id': promo_code.id,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_my_active_promocodes(request):
    """
    Получить список активированных, но ещё не применённых промокодов пользователя.
    """
    activations = UserPromoCodeActivation.objects.filter(
        user=request.user,
        is_applied=False
    ).select_related('promocode', 'promocode__bonus_type')

    data = []
    for act in activations:
        promo = act.promocode
        data.append({
            'id': act.id,
            'promocode_id': promo.id,
            'code': promo.code,
            'created_at': act.created_at,
            'bonuses': [
                {
                    'type': b.bonus_type.code,
                    'amount': b.amount,
                    'description': b.bonus_type.description
                }
                for b in promo.bonuses.all()
            ]
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def confirm_promocode_rewards(request):
    """
    Подтвердить получение бонусов по активированному промокоду.
    После этого бонусы считаются начисленными.
    """
    activation_id = request.data.get('activation_id')

    if not activation_id:
        return Response(
            {'error': 'Требуется activation_id.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        activation = UserPromoCodeActivation.objects.get(
            id=activation_id,
            user=request.user,
            is_applied=False
        )
    except UserPromoCodeActivation.DoesNotExist:
        return Response(
            {'error': 'Активация не найдена или бонусы уже начислены.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Здесь можно вызвать сервис по начислению бонусов
    # Например: give_bonuses_to_user(activation.user, activation.promocode.bonuses)

    activation.is_applied = True
    activation.applied_at = timezone.now()
    activation.save()

    return Response({
        'success': True,
        'message': 'Бонусы успешно подтверждены и начислены.'
    }, status=status.HTTP_200_OK)