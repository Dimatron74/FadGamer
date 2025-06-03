# main/models.py
from django.db import models



# Тип продуктов
class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

# Продукты
class Products(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Описание', blank=True)
    cover_image = models.ImageField('Обложка', upload_to='products/covers/', null=True, blank=True)
    release_date = models.DateField('Дата выхода', null=True, blank=True)
    is_published = models.BooleanField('Опубликовано', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

# Сервисы
class Service(models.Model):
    name = models.CharField(unique=True, max_length=255)
    icon = models.ImageField('Иконка', upload_to='services/icons/', null=True, blank=True)

    def __str__(self):
        return self.name
    
# Где приобрести    
class AcquisitionMethod(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='acquisition_methods')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    url = models.URLField('Ссылка', help_text='Внешняя или внутренняя ссылка')
    is_internal = models.BooleanField(default=False, help_text='Является ли ссылка внутренней (сайт студии)')

    def __str__(self):
        return f'{self.product.name} - {self.service.name}'