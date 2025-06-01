# profiles/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserEmail

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