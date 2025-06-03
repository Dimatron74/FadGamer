# profiles/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserEmail, UserProducts
from ..games.models import Game

class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email и пароль обязательны.')

        # Ищем пользователя с активным email
        user_email_entry = UserEmail.objects.filter(email__email=email, is_active=True).first()

        if not user_email_entry:
            raise serializers.ValidationError('Пользователь с таким email не найден или не активирован.')

        user = user_email_entry.user

        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль.')

        refresh = RefreshToken.for_user(user)
        refresh['user'] = user.nickname  # Добавляем nickname в payload токена

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'nickname': user.nickname,
        }
    
class ProductUserSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    cover_image = serializers.SerializerMethodField()
    distribution_model = serializers.CharField(source='distribution_model.name')
    is_game = serializers.SerializerMethodField()

    class Meta:
        model = UserProducts
        fields = [
            'id', 'product_name', 'cover_image', 'created_at',
            'is_blocked', 'distribution_model', 'last_login',
            'is_game'
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.product.cover_image and hasattr(obj.product.cover_image, 'url'):
            return request.build_absolute_uri(obj.product.cover_image.url)
        return None

    def get_is_game(self, obj):
        # Проверяем, является ли продукт экземпляром модели Game
        return hasattr(obj.product, 'game') and isinstance(obj.product.game, Game)