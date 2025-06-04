# apps/main/serializers.py
from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']

class AcquisitionMethodSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = AcquisitionMethod
        fields = ['id', 'service', 'url', 'is_internal']

class ProductSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    product_type = serializers.CharField(source='product_type.name', read_only=True)

    class Meta:
        model = Products
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'cover_image',
            'cover_image_url',
            'product_type',
            'is_published'
        ]
        read_only_fields = ['is_published']

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None
    
class SentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentEmail
        fields = ['id', 'recipient', 'subject', 'body', 'sent_at', 'is_sent', 'error_message']
        read_only_fields = fields

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'subject', 'body', 'html_body', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']