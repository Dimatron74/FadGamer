from rest_framework import serializers
from .models import Service, Category, Ticket, Message, MessageAttachment

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'service', 'name', 'slug', 'description']

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'uploaded_at']

class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'ticket', 'author', 'sender_type', 'text', 'created_at', 'attachments']

class TicketSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    service = ServiceSerializer()
    category = CategorySerializer()

    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'service', 'category', 'title', 
            'description', 'status', 'created_at', 'updated_at', 'messages'
        ]