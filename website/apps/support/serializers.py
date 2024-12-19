from rest_framework import serializers
from .models import SupportRequest

class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ['id', 'question', 'text', 'answer', 'answered', 'created_at', 'updated_at', 'user']
        read_only_fields = ['created_at', 'updated_at']  # только для чтения
