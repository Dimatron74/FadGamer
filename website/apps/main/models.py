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
    
    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
    
# Где приобрести    
class AcquisitionMethod(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='acquisition_methods')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    url = models.URLField('Ссылка', help_text='Внешняя или внутренняя ссылка')
    is_internal = models.BooleanField(default=False, help_text='Является ли ссылка внутренней (сайт студии)')

    def __str__(self):
        return f'{self.product.name} - {self.service.name}'
    
    class Meta:
        verbose_name = 'Метод приобретения'
        verbose_name_plural = 'Методы приобретения'

class EmailTemplate(models.Model):
    name = models.CharField('Название шаблона', max_length=100, unique=True)
    subject = models.CharField('Тема письма', max_length=255)
    body = models.TextField('Тело письма')
    html_body = models.TextField('HTML тело письма', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаблон электронного письма'
        verbose_name_plural = 'Шаблоны электронных писем'

class SentEmail(models.Model):
    recipient = models.EmailField('Получатель')
    subject = models.CharField('Тема', max_length=255)
    body = models.TextField('Содержание')
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Письмо на {self.recipient} ({'отправлено' if self.is_sent else 'ошибка'})"

    class Meta:
        verbose_name = 'Отправленное письмо'
        verbose_name_plural = 'Отправленные письма'