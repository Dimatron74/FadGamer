from rest_framework import serializers
from .models import Service, Category, Ticket, Message, MessageAttachment
# from ..profiles.models import User
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

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
    author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'ticket', 'author', 'sender_type', 'text', 'created_at', 'attachments', 'is_deleted']
        read_only_fields = ['ticket', 'author', 'sender_type', 'created_at', 'attachments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # При обновлении делаем text и sender_type read-only
        if self.context['request'].method in ['PUT', 'PATCH']:
            for field in ['text', 'sender_type']:
                self.fields[field].read_only = True
    
    def get_author(self, obj):
        if obj.author and obj.sender_type !='ai':
            return {
                "nickname": obj.author.nickname,
                "uid": obj.author.uid
            }
        return None

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    service_name = serializers.CharField(source='service.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    messages_count = serializers.SerializerMethodField()
    last_message_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'service', 'category', 'title',
            'description', 'status', 'created_at', 'updated_at', 
            'messages_count', 'service_name', 'category_name', 'last_message_time',
        ]

    def get_user(self, obj):
        return {
            'uid': obj.user.uid,
            'nickname': obj.user.nickname,
        }
    def get_category_service(self, obj):
        return {
            'category': obj.user.uid,
            'service': obj.user.nickname,
        }
    
    def get_messages_count(self, obj):
        request = self.context.get('request')

        # Если запрос из админки — считаем все сообщения
        if '/admin/' in request.path if request else False:
            return obj.messages.count() + 1

        # Иначе — только не удалённые
        return obj.messages.filter(is_deleted=False).count() + 1