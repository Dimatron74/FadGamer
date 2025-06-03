# apps/main/serializers.py
from rest_framework import serializers
from .models import AcquisitionMethod, Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']

class AcquisitionMethodSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = AcquisitionMethod
        fields = ['id', 'service', 'url', 'is_internal']