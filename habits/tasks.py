from config import settings
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import Celery
import requests


app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def send_telegram_message(chat_id, habit_name):
    """ Отправка рассылки в телеграм с именем привычки. """
    params = {
        'text': f'Не забудьте выполнить действие для привычки: {habit_name}.',
        'chat_id': chat_id,
    }
    requests.get(f"{settings.TELEGRAM_URL}{settings.BOT_TOKEN}/sendMessage", params=params)


@app.task
def reminder_of_habit(habit_id, chat_id, habit_name, periodicity):
    """ Задача по расписанию: отправляет напоминание пользователю о выполнении привычки """

    # Создаем интервал для повтора
    schedule, created = IntervalSchedule.objects.get_or_create(
         every=periodicity,
         period=IntervalSchedule.DAYS,
     )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
         interval=schedule,
         name=f'Напоминание о {habit_name} для {chat_id}',
         task='habits.tasks.send_telegram_message',
         args=[chat_id, habit_name, habit_id],
     )

    # celery -A config worker -l INFO -P eventlet
    # celery -A config beat -l INFO -S django -P eventlet
