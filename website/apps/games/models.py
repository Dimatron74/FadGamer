# games/models.py
from django.db import models
from ..main.models import Products

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Game(Products):  # Наследуется от Product
    genres = models.ManyToManyField(Genre, related_name='games')
    platforms = models.ManyToManyField(Platform, related_name='games')
    features = models.ManyToManyField(Feature, related_name='games')
    how_to_get = models.TextField('Как получить', blank=True)
    trailer_url = models.URLField('Ссылка на трейлер', blank=True)

    def __str__(self):
        return f"Игра: {self.name}"

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'