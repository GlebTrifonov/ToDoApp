# Базовый образ - пайто 3.12 слим
FROM python:3.12-slim
# Рабочая директория внутри контейнера
WORKDIR /app
# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    #  gcc — компилятор (нужен для некоторых пакетов(каких - не знаю))
    gcc \
    #  libpq-dev — для подключения к PostgreSQL
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
#Копируем файл с зависимостями 
COPY requirements.txt .
# Устанавливаем Python-пакеты
RUN pip install --upgrade pip && pip install -r requirements.txt
# Копируем все остальное(код)
COPY . .
# Открываем порт
EXPOSE 8000
# Запускаем кодманду при старте контейнера
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]