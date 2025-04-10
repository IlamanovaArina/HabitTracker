from datetime import time
from django.db import models
from config import settings


class Award(models.Model):
    """ Модель вознаграждения """
    name = models.CharField()


class Habits(models.Model):
    """ Модель привычки. Приятной иои полезной. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                             related_name='owner_lesson', verbose_name='Пользователь')
    place = models.CharField(max_length=100, help_text='Место в котором необходимо выполнять действие.')
    tame = models.TimeField(help_text='Время, когда не обходимо выполнять действие.')
    action = models.CharField(max_length=250, help_text='Само действие')
    pleasant_habits_sign = models.BooleanField(blank=True, null=True,
                                               help_text='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                      help_text='Связанная привычка')
    periodicity = models.IntegerField(help_text='Периодичность(в днях)', default=2)
    award = models.ForeignKey(Award, on_delete=models.SET_NULL, blank=True, null=True, help_text='Вознаграждение')
    time_to_complete = models.DurationField(default=time(minute=1, hour=0), help_text='Время на выполнение')
    sign_of_publicity = models.BooleanField(default=False, help_text='Признак публичности')
