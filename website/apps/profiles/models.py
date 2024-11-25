import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_role(cls):
        return cls.objects.get_or_create(name='user')[0]

class Email(models.Model):
    email = models.EmailField(unique=True, primary_key=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name='email')
    binding_date = models.DateTimeField(auto_now_add=True)

    NOTIFICATION_CHOICES = [
        ('all', 'All Notifications'),
        ('important', 'Important Notifications Only'),
        ('none', 'No Notifications'),
    ]
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES, default='all')

    def __str__(self):
        return self.email



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    nickname = models.CharField(unique=True, max_length=255)
    email = models.OneToOneField(Email, on_delete=models.CASCADE, related_name='user')
    password = models.CharField(max_length=255)
    avatar = models.BinaryField(null=True)
    birth_date = models.DateTimeField(null=True)
    phone_number = models.CharField(null=True, max_length=20)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        if not self.roles.exists():
            self.roles.add(Role.get_default_role())
        super().save(*args, **kwargs)

