# news/models.py

from django.db import models
from apps.main.models import Products

class News(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('Slug', unique=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    short_description = models.TextField('Краткое описание', blank=True)
    cover_image = models.ImageField('Обложка', upload_to='news/covers/', null=True, blank=True)
    is_published = models.BooleanField('Опубликовано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class NewsBlock(models.Model):
    BLOCK_TYPES = (
        ('text', 'Текст'),
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('quote', 'Цитата'),
    )

    news = models.ForeignKey(News, related_name='blocks', on_delete=models.CASCADE)
    block_type = models.CharField('Тип блока', max_length=10, choices=BLOCK_TYPES)
    content = models.TextField('Содержимое', blank=True)
    image = models.ImageField('Изображение', upload_to='news/blocks/images/', null=True, blank=True)
    video_url = models.URLField('Ссылка на видео', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    def __str__(self):
        return f'{self.news.title} - {self.block_type}'

    class Meta:
        ordering = ['order']
        verbose_name = 'Блок новости'
        verbose_name_plural = 'Блоки новостей'