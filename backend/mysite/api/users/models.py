from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        max_length=254
    )
    username = models.CharField(
        'Ник',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        blank=True
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
    )

    object = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.username
