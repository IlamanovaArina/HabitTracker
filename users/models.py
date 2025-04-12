from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователя """
    username = None
    name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Номер телефона')
    tg_chat_id = models.CharField(blank=True, null=True, verbose_name='Телеграм чат-id',
                                  help_text='Укажите телеграм чат-id')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
