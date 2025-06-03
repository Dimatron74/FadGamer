# apps/games/admin.py
from django.contrib import admin
from .models import Game, Genre, Platform, Feature

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_published']
    list_filter = ['is_published', 'genres', 'platforms']
    filter_horizontal = ['genres', 'platforms', 'features']
    prepopulated_fields = {'slug': ('name',)}