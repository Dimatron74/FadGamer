# apps/admin_panel/serializers.py

from rest_framework import serializers
from .models import PromoCode, PromoCodeBonus, BonusType, UserPromoCodeActivation
from ..support.models import Products
from ..profiles.models import User
from django.utils import timezone
from apps.news.models import News, NewsBlock
from apps.main.serializers import ProductSerializer

class BonusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusType
        fields = ['id', 'code', 'name', 'is_amount']


class PromoCodeBonusSerializer(serializers.ModelSerializer):
    bonus_type = BonusTypeSerializer(read_only=True)
    bonus_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BonusType.objects.all(),
        source='bonus_type',
        write_only=True
    )

    class Meta:
        model = PromoCodeBonus
        fields = ['id', 'bonus_type', 'bonus_type_id', 'amount']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name']


class PromoCodeSerializer(serializers.ModelSerializer):
    bonuses = PromoCodeBonusSerializer(many=True)
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(),
        source='service',
        write_only=True
    )
    author = serializers.SerializerMethodField()

    class Meta:
        model = PromoCode
        fields = [
            'id', 'code', 'status', 'service', 'service_id',
            'created_at', 'expires_at', 'author', 'bonuses', 'max_activations'
        ]
        read_only_fields = ['author']

    def get_author(self, obj):
        if obj.author:
            return {
                "nickname": obj.author.nickname,
                "uid": obj.author.uid
            }
        return None

    def validate_status(self, value):
        if not self.instance and value not in ['active', 'inactive']:
            raise serializers.ValidationError("При создании статус должен быть 'active' или 'inactive'")
        return value

    def validate_created_at(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Дата активации не может быть в прошлом")
        return value

    def update(self, instance, validated_data):
        # При обновлении разрешено менять только status
        status = validated_data.get('status')
        if status is not None:
            instance.status = status
        instance.save()
        return instance

    def create(self, validated_data):
        bonuses_data = validated_data.pop('bonuses')
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        promo_code = PromoCode.objects.create(author=user, **validated_data)
        for bonus_data in bonuses_data:
            PromoCodeBonus.objects.create(promocode=promo_code, **bonus_data)
        return promo_code


class UserPromoCodeActivationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='nickname', read_only=True)
    promocode = serializers.StringRelatedField()

    class Meta:
        model = UserPromoCodeActivation
        fields = ['id', 'user', 'promocode', 'activated_at', 'is_applied']

class NewsBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsBlock
        fields = ['id', 'block_type', 'content', 'image', 'video_url', 'order']


class NewsSerializer(serializers.ModelSerializer):
    blocks = NewsBlockSerializer(many=True, required=False)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'short_description', 'cover_image', 'product',
                  'is_published', 'created_at', 'updated_at', 'blocks']