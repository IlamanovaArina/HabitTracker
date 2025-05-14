# Указываем базовый образ
FROM python:3.12.5-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /HabitTracker

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем остальные файлы проекта в контейнер
COPY . .

# Создать необходимые директории для хранения медиафайлов и статических файлов приложения.
# Обеспечить правильные права доступа, чтобы сервер или приложение могли читать и писать в эти папки.
RUN mkdir -p ./media && chmod -R 755 /media
RUN mkdir -p ./staticfiles && chmod -R 755 /staticfiles

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]