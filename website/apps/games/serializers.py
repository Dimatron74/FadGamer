# apps/games/serializers.py
from rest_framework import serializers
from ..main.models import Service
from ..main.serializers import AcquisitionMethodSerializer
from .models import Game, Genre, Platform, Feature

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']

class GameSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    platforms = PlatformSerializer(many=True)
    features = FeatureSerializer(many=True)
    acquisition_methods = AcquisitionMethodSerializer(many=True)
    is_game = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id', 'name', 'slug', 'description', 'cover_image',
            'release_date', 'is_published', 'genres', 'platforms',
            'trailer_url', 'acquisition_methods', 'is_game', 'features',
        ]

    def get_is_game(self, obj):
        return True