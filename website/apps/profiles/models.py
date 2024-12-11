import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        if not nickname:
            raise ValueError('The Nickname field must be set')
        nickname = self.normalize_email(nickname)
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
    name = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_role(cls):
        return cls.objects.get_or_create(name='user')[0]
    
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
    name = models.CharField(unique=True)

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


class AccountLock(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="locked_accounts")
    blocked_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="blocked_accounts", null=True, blank=True)
    reason = models.CharField(default="Без причины", max_length=255)
    blocked_at = models.DateTimeField(auto_now_add=True)
    unblocked_at = models.DateTimeField(null=True, blank=True)
    is_unblocked = models.BooleanField(default=False)

    def __str__(self):
        return f'Аккаунт {self.user.nickname} был заблокирован по причине: {self.reason}'









class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    nickname = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateTimeField(null=True)
    phone_number = models.CharField(null=True, max_length=20)
    is_blocked = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    NOTIFICATION_CHOICES = [
        ('all', 'All Notifications'),
        ('important', 'Important Notifications Only'),
        ('none', 'No Notifications'),
    ]
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES, default='all')

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []
    
    def get_current_email(self):
        return self.emails.filter(is_active=True).latest('binding_date')

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем объект self в базе данных
        # using = kwargs.get('using')
        # print(using)
        # default_role = Role.objects.using(using).get_or_create(name='user')[0]
        default_role = Role.objects.get_or_create(name='user')[0]
        if not self.roles.exists():
            self.roles.add(default_role)


