# ToDo App

Простое приложение для управления задачами на Django с поддержкой Docker.

## Технологии

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
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
   venv\Scripts\activate  # Windows

2. Зависимости
    pip install -r requirements.txt

3. Миграции
    python manage.py migrate

4. СОздание суперюзера для админки
    python manage.py createsuperuser

5. Запускаем сервер
    python manage.py runserver

                """     ЗАПУСК ЧЕРЕЗ DOCKER !!!          """

1. СБОРКА И ЗАПУСК КОНТЕЙНЕРА
    docker-compose up --build

2. МИГРАЦИИ В НОВОМ ТЕРМИНАЛЕ(не в открывшимся)
    docker-compose exec app python manage.py migrage

3. СОЗДАНИЕ СУПЕРЮЗЕРА ЧЕРЕЗ ДОКЕР
    docker-compose exec app python manage.py createsuperuser

4. ОТКРЫТЬ САЙТ:
    http://localhost:8000


                """     ТЕСТЫ !!!          """           
1. БЕЗ ДОКЕР
    pytest

2. С ДОКЕРОМ
    docker-compose exec app pytest


                """     СТРУКТУРА ПРОЕКТА          """                

ToDoApp/
├── .devcontainer/       # Конфигурация Codespace
├── .github/             # GitHub Actions (CI)
├── api/                 # DRF API
├── core/                # Настройки проекта
├── tests/               # Тесты (pytest)
├── todo/                # Основное приложение
├── users/               # Авторизация
├── Dockerfile           # Сборка образа
├── docker-compose.yml   # Оркестрация контейнеров
├── requirements.txt     # Зависимости
└── manage.py