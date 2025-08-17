# support/models.py
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..main.models import Products



# ==== Категории запросов ====
class Category(models.Model):
    service = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Продукт'
    )
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Slug')
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return f"{self.service.name}: {self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('service', 'slug')


# ==== Тикет техподдержки ====
class Ticket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Ожидает ответа'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыт'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Пользователь'
    )
    service = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tickets',
        verbose_name='Сервис'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tickets',
        verbose_name='Категория'
    )

    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)
    last_message_time = models.DateTimeField('Время последнего сообщения', null=True, blank=True)

    def update_last_message_time(self, message_time=None):
        """
        Обновляет last_message_time.
        Если message_time не передан — используется created_at тикета (для первого сообщения).
        """
        self.last_message_time = message_time or self.created_at
        self.save(update_fields=['last_message_time'])

    def __str__(self):
        return f"{self.title} ({self.user})"

    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'


# ==== Сообщение в тикете ====
SENDER_TYPE_CHOICES = (
    ('user', 'Пользователь'),
    ('staff', 'Сотрудник'),
    ('ai', 'AI-бот'),
)


class Message(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Тикет'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор'
    )
    sender_type = models.CharField(
        'Тип отправителя',
        max_length=10,
        choices=SENDER_TYPE_CHOICES,
        default='user'
    )
    text = models.TextField('Текст сообщения')
    created_at = models.DateTimeField('Дата', default=now)
    is_deleted = models.BooleanField('Удалено', default=False)

    def __str__(self):
        return f"Сообщение от {self.get_sender_type_display()}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


# ==== Файлы к сообщениям ====
class MessageAttachment(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Сообщение'
    )
    file = models.FileField('Файл', upload_to='support_attachments/messages/')
    uploaded_at = models.DateTimeField('Загружено', auto_now_add=True)

    def __str__(self):
        return f"Файл для сообщения #{self.message.id}"

    class Meta:
        verbose_name = 'Файл к сообщению'
        verbose_name_plural = 'Файлы к сообщениям'



# Сигналы

@receiver(post_save, sender=Ticket)
def set_initial_last_message_time(sender, instance, created, **kwargs):
    """Если тикет только создан — устанавливаем last_message_time = created_at"""
    if created:
        instance.update_last_message_time(message_time=instance.created_at)


@receiver(post_save, sender=Message)
def update_ticket_last_message(sender, instance, created, **kwargs):
    """При добавлении нового сообщения — обновляем last_message_time"""
    if created and not instance.is_deleted:
        ticket = instance.ticket
        ticket.update_last_message_time(message_time=instance.created_at)