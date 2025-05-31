# apps/admin_panel/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from ..profiles.models import User
from ..support.models import Service


class BonusType(models.Model):
    """
    Типы бонусов, которые могут быть у промокода.
    Например: монеты, скин, премиум и т.д.
    """
    code = models.CharField('Код', max_length=50, unique=True)
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    is_amount = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип бонуса'
        verbose_name_plural = 'Типы бонусов'


class PromoCode(models.Model):
    """
    Промокод.
    """
    STATUS_CHOICES = (
        ('active', 'Активный'),
        ('inactive', 'Неактивный'),
        ('used', 'Использованный'),
        ('expired', 'Истекший'),
        ('closed', 'Завершённый'),
    )

    code = models.CharField('Промокод', max_length=50, unique=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='promocodes',
        verbose_name='Сервис/игра'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    expires_at = models.DateTimeField('Дата истечения', null=True, blank=True)
    max_activations = models.PositiveIntegerField('Количество активаций', null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_promocodes',
        verbose_name='Автор'
    )

    def __str__(self):
        return f"{self.code} ({self.status})"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def save(self, *args, **kwargs):
        # Если статус "inactive", и created_at ещё не задан — можно оставить None
        if self.status == 'inactive' and not self.created_at:
            pass  # может быть установлено вручную
        elif not self.id:  # новая запись
            self.created_at = timezone.now()
        super().save(*args, **kwargs)


class PromoCodeBonus(models.Model):
    """
    Бонус для промокода (например: +50 монет, +1 скин).
    """
    promocode = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        related_name='bonuses',
        verbose_name='Промокод'
    )
    bonus_type = models.ForeignKey(
        BonusType,
        on_delete=models.CASCADE,
        verbose_name='Тип бонуса'
    )
    amount = models.PositiveIntegerField('Количество', null=True, blank=True)

    def __str__(self):
        return f"{self.bonus_type.name}: {self.amount or '-'}"

    class Meta:
        verbose_name = 'Бонус промокода'
        verbose_name_plural = 'Бонусы промокодов'


class UserPromoCodeActivation(models.Model):
    """
    Активация пользователем промокода.
    Ограничивает двойное использование.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activated_promocodes',
        verbose_name='Пользователь'
    )
    promocode = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        related_name='activations',
        verbose_name='Промокод'
    )
    activated_at = models.DateTimeField('Дата активации', auto_now_add=True)
    is_applied = models.BooleanField('Начислено', default=False)

    def __str__(self):
        return f"{self.user.nickname} - {self.promocode.code}"

    class Meta:
        verbose_name = 'Активация промокода'
        verbose_name_plural = 'Активации промокодов'
        unique_together = ('user', 'promocode')