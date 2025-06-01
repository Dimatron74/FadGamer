# profiles/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserEmail

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = user.nickname
        data = {
            'refresh': str(token),
            'access': str(token.access_token),
            'nickname': token['user']
        }
        return data
    

    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'] = self.fields.pop('nickname')
        self.fields.pop('nickname')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user_email = UserEmail.objects.filter(email__email=email).first()
        if user_email and user_email.user.check_password(password):
            return attrs
        else:
            raise serializers.ValidationError('Не найдено активной учетной записи с указанными данными')