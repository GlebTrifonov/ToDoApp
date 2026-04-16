# Docker для Django

## Основные команды
- `docker-compose up --build` — собрать и запустить
- `docker-compose down` — остановить
- `docker-compose down -v` — остановить и удалить БД
- `docker-compose exec app python manage.py migrate` — миграции
- `docker-compose exec app python manage.py createsuperuser` — суперпользователь

## Структура Dockerfile
- FROM — базовый образ
- WORKDIR — рабочая папка
- COPY — копирование файлов
- RUN — команды при сборке
- CMD — команда при запуске

## Структура docker-compose.yml
- services.db — PostgreSQL
- services.app — Django
- environment — переменные окружения
- ports — проброс портов
- depends_on — порядок запуска
- volumes — сохранение данных