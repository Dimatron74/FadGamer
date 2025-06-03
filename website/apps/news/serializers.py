from rest_framework import serializers
from .models import News, NewsBlock
from apps.main.serializers import ProductSerializer

class NewsBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsBlock
        fields = ['id', 'block_type', 'content', 'image', 'video_url', 'order']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            request = self.context.get('request')
            data['image'] = request.build_absolute_uri(instance.image.url)
        return data


class NewsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    blocks = NewsBlockSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'short_description', 'cover_image', 'product', 'is_published', 'created_at', 'updated_at', 'blocks']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.cover_image:
            request = self.context.get('request')
            data['cover_image'] = request.build_absolute_uri(instance.cover_image.url)
        return data