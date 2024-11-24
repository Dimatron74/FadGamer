import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.IntegerField()
    nickname = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    avatar = models.BinaryField(null=True)
    birth_date = models.DateTimeField(null=True)
    phone_number = models.CharField(null=True, max_length=20)
    is_blocked = models.BooleanField(default=False)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    @property
    def is_staff(self):
        return self.role == 1


