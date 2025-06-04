#contact/serializers.py

from rest_framework import serializers
from .models import ContactRequest
from apps.profiles.models import Email, UserEmail, User

class ContactRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=False)
    guest_email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContactRequest
        fields = [
            'id', 'user', 'name', 'email',
            'subject', 'message', 'is_resolved',
            'admin_response', 'created_at', 'responded_at', 'guest_email'
        ]
        read_only_fields = ['id', 'created_at', 'responded_at', 'guest_email']

    def get_guest_email(self, obj):
        return obj.email.email if obj.email else None

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        user = validated_data.get('user')

        # Если пользователь авторизован — берем его email
        if user and not email:
            userEmail = UserEmail.objects.filter(user=user, is_active=True).first()
            if userEmail:
                validated_data['email'] = userEmail.email

        # Если пользователь НЕ авторизован — создаём email
        elif not user and email:
            try:
                email_obj, _ = Email.objects.get_or_create(email=email)
                validated_data['email'] = email_obj
            except Exception as e:
                raise serializers.ValidationError(f"Ошибка при создании email: {e}")

        return super().create(validated_data)