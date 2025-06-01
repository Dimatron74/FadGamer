# profiles/models.py

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from phonenumber_field.modelfields import PhoneNumberField
from ..main.models import Products



class UserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        if not nickname:
            raise ValueError('The Nickname field must be set')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(nickname, password, **extra_fields)

    def get_by_natural_key(self, nickname):
        return self.get(nickname=nickname)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='role', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Создаём или обновляем связанную группу
        if not self.group:
            self.group, _ = Group.objects.get_or_create(name=self.name)
        super().save(*args, **kwargs)

    @classmethod
    def get_default_role(cls):
        role, created = cls.objects.get_or_create(name='user', defaults={'description': 'Default user role'})
        return role

class Email(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class UserEmail(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'email')

    def __str__(self):
        return f'{self.user.nickname} - {self.email.email}'

class Service(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name

class UserService(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'service')

    def __str__(self):
        return f'{self.user.nickname} - {self.service.name}'
    
class UserProducts(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    DISTRIBUTION_CHOICES = [
        ('pay', 'Платная лицензия'),
        ('free', 'Бесплатная лицензия'),
        ('none', 'Без модели'),
    ]
    distribution_model = models.CharField(max_length=50, choices=DISTRIBUTION_CHOICES, default='none')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.nickname} - {self.product.name}'

class AccountLock(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="locked_accounts")
    blocked_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="blocked_accounts", null=True, blank=True)
    reason = models.CharField(default="Без причины", max_length=255)
    blocked_at = models.DateTimeField(auto_now_add=True)
    unblocked_at = models.DateTimeField(null=True, blank=True)
    is_unblocked = models.BooleanField(default=False)

    def __str__(self):
        return f'Аккаунт {self.user.nickname} заблокирован по причине: {self.reason}'

class UIDCounter(models.Model):
    server_prefix = models.CharField(max_length=2, unique=True)
    sequence_number = models.BigIntegerField(default=0)

    @classmethod
    def get_next_uid(cls, server_prefix="1"):
        counter, created = cls.objects.get_or_create(server_prefix=server_prefix, defaults={'sequence_number': 0})
        counter.sequence_number += 1
        counter.save()
        return counter.sequence_number

def generate_uid(server_prefix="1"):
    sequence = UIDCounter.get_next_uid(server_prefix)
    return f"{server_prefix}{sequence:010d}"






class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=12, primary_key=True, unique=True, editable=False)
    nickname = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    NOTIFICATION_CHOICES = [
        ('all', 'All Notifications'),
        ('important', 'Important Notifications Only'),
        ('none', 'No Notifications'),
    ]
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES, default='all')

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.uid:  # Генерируем UID только при создании
            self.uid = generate_uid()
        super().save(*args, **kwargs)
        # Назначаем роль по умолчанию
        default_role = Role.get_default_role()
        if not self.groups.filter(name=default_role.name).exists():
            self.groups.add(default_role.group)

    def get_active_email(self):
        userEmail = self.useremail_set.filter(is_active=True).first()
        return userEmail.email.email if userEmail else None

    def __str__(self):
        return f"{self.nickname} ({self.uid})"

