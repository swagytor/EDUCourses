from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='Почта', unique=True)

    phone = models.CharField(max_length=100, verbose_name='Телефон')
    town = models.CharField(max_length=100, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
