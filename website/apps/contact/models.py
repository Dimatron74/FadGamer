# contact/models.py

from django.db import models
from apps.profiles.models import User, Email

class ContactRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Имя', max_length=100, blank=True)
    subject = models.CharField('Тема', max_length=255)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField('Закрыто', default=False)
    admin_response = models.TextField('Ответ администратора', blank=True, null=True)
    responded_at = models.DateTimeField('Дата ответа', null=True, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.created_at})"

    class Meta:
        verbose_name = 'Запрос связи'
        verbose_name_plural = 'Запросы связи'