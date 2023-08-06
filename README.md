
# Проект foodgram

[![site build status](https://github.com/ffff00-korj/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://corgxes-gram.ru)

Foodgram - это социальная платформа для любителей еды, где вы можете делиться
своими любимыми рецептами, подписываться на авторов, добавлять их в избранное
и выгружать рецепты как список покупок.

## Особенности проекта

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление рецептов
- Поиск рецептов по названию и ингредиентам
- Подписка на авторов и просмотр их рецептов
- Добавление рецептов в избранное
- Выгрузка рецептов в формате списка покупок

## Технологии

- Python 3.9.11
- Django 3.2
- Django REST framework 3.14
- PostgreSQL 13
- Docker

## Установка

### Склонируйте репозиторий

```txt
git clone https://github.com/ffff00-korj/foodgram-project-react.git
```

### Создайте файл .env с переменными окружения

```env
DJANGO_SECRET_KEY='django-insecure-802o==dsajkldjk#@$&()*GOIhno32RH{F*()FH)@*(#:2'
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS='127.0.0.1 0.0.0.0 localhost'

DB_HOST=db
DB_PORT=5432

POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram
POSTGRES_DB=foodgram

SQLITE_ENGINE=0
```

### Перейдите в каталог infra

```bash
cd infra/
```

### Запустите приложение с помощью docker-compose

```bash
docker-compose up -d --build
```

### Примените миграции:

```bash
docker-compose exec backend python manage.py migrate --noinput
```

### Создайте суперпользователя

```bash
docker-compose exec backend python manage.py createsuperuser
```

### Откройте приложение в браузере

```bash
http://localhost/
```

## Авторы

- Илья Боровков
- Яндекс-практикум
