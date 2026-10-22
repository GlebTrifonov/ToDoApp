# ToDo App

Приложение для управления задачами на Django: веб-интерфейс и REST API, фоновые задачи на Celery, запуск в Docker.

## Технологии

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- Celery + Redis (автоудаление истории задач)
- Docker / Docker Compose
- pytest (тесты)
- GitHub Actions (CI)

## Быстрый старт

### Локальная разработка (без Docker)

1. Создай виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

2. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Примени миграции:
   ```bash
   python manage.py migrate
   ```

4. Создай суперпользователя для админки:
   ```bash
   python manage.py createsuperuser
   ```

5. Запусти сервер (для разработки включи `DEBUG`):
   ```bash
   export DJANGO_DEBUG=True   # Windows: set DJANGO_DEBUG=True
   python manage.py runserver
   ```

Настройки берутся из переменных окружения: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `POSTGRES_*`.

### Запуск через Docker

1. Собери и запусти контейнеры:
   ```bash
   docker-compose up --build
   ```

2. В новом терминале примени миграции:
   ```bash
   docker-compose exec app python manage.py migrate
   ```

3. Создай суперпользователя:
   ```bash
   docker-compose exec app python manage.py createsuperuser
   ```

4. Открой сайт: http://localhost:8000

## Тесты

```bash
pytest                            # без Docker
docker-compose exec app pytest    # в Docker
```

## Структура проекта

```
ToDoApp/
├── .devcontainer/       # Конфигурация Codespace
├── .github/             # GitHub Actions (CI)
├── api/                 # DRF API
├── core/                # Настройки проекта, Celery
├── tests/               # Тесты (pytest)
├── todo/                # Основное приложение
├── users/               # Авторизация
├── Dockerfile           # Сборка образа
├── docker-compose.yml   # Оркестрация контейнеров
├── requirements.txt     # Зависимости
└── manage.py
```
