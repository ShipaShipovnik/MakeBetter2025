from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("The Login must be set")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Числовой ID
    email = models.EmailField(unique=True, blank=True, null=True)  # Почта теперь не обязательна
    name = models.CharField(max_length=255, blank=True, default='')
    login = models.CharField(max_length=100, unique=True)  # Поле логина как username

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.login