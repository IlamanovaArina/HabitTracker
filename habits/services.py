# import requests
#
# from config import settings
#
#
# def send_telegram_message(chat_id):
#     """ Отправка рассылки в телеграмм """
#     params = {
#         'text': 'Не забудьте выполнить действие для привития полезной привычки.',
#         'chat_id': chat_id,
#     }
#     response = requests.get(f"{settings.TELEGRAM_URL}{settings.BOT_TOKEN}/sendMessage", params=params)
