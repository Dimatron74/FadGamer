# admin_panel/api.py

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ..news.serializers import NewsSerializer
from ..news.models import News
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserPromoCodeActivation


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
def confirm_promocode_rewards(request):
    promo_code_id = request.data.get('promo_code_id')

    if not promo_code_id:
        return Response({'error': 'Не указан ID промокода'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        activation = UserPromoCodeActivation.objects.get(
            user=request.user,
            promocode_id=promo_code_id,
            is_applied=False
        )
    except UserPromoCodeActivation.DoesNotExist:
        return Response({'error': 'Промокод не найден или уже применён'}, status=status.HTTP_400_BAD_REQUEST)

    # Подтверждаем начисление бонусов
    activation.is_applied = True
    activation.save()

    return Response({'success': 'Бонусы успешно начислены'}, status=status.HTTP_200_OK)