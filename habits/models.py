import datetime
from django.db import models
from users.models import User


class Award(models.Model):
    """ Модель вознаграждения """

    name = models.CharField(max_length=100, help_text='Название')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Владелец')
    description = models.TextField(max_length=200, blank=True, null=True, help_text='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')


class Habits(models.Model):
    """ Модель привычки. Приятной иои полезной. """
    name = models.CharField(max_length=50, blank=True, null=True, help_text='Название привычки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='habits', verbose_name='Пользователь')
    place = models.CharField(max_length=100, help_text='Место в котором необходимо выполнять действие.')
    time = models.TimeField(help_text='Время, когда не обходимо выполнять действие.')
    action = models.CharField(max_length=250, help_text='Само действие')
    pleasant_habits_sign = models.BooleanField(default=False,
                                               help_text='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                      help_text='Связанная привычка')
    periodicity = models.IntegerField(help_text='Периодичность(в днях)', default=2)
    award = models.ForeignKey(Award, on_delete=models.SET_NULL, blank=True, null=True, help_text='Вознаграждение')
    time_to_complete = models.DurationField(default=datetime.time(minute=1, hour=0), help_text='Время на выполнение')
    is_public = models.BooleanField(default=False, help_text='Признак публичности')
