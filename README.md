# Проект foodgram
[![site build status](https://github.com/ffff00-korj/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://corgxes-gram.ru)


Foodgram - это социальная платформа для любителей еды, где вы можете делиться своими любимыми рецептами, подписываться на авторов, добавлять их в избранное и выгружать рецепты как список покупок.


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
- Django REST framework 3.14.0
- PostgreSQL 13
- Docker

## Установка

1. Склонируйте репозиторий:


```txt
git clone https://github.com/ffff00-korj/foodgram-project-react.git
```


2. Создайте файл .env с переменными окружения:

```txt
DEBUG=0
DB_NAME=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

3. Перейдите в каталог infra

```bash
cd infra/
```

3. Запустите приложение с помощью docker-compose:

```bash
docker-compose up -d --build
```

4. Примените миграции:

```bash
docker-compose exec backend python manage.py migrate --noinput
```

5. Создайте суперпользователя:

```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Откройте приложение в браузере:

```bash
http://localhost/
```

## Авторы

- Илья Боровков
- Яндекс-практикум

