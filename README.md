![example workflow](https://github.com/Enh404/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Описание проекта:

Данный проект это API версия блога Yatube. Теперь, с помощью различных запросов к эндпойнтам (например в Postman) можно получать информацию, которая содержится на сайте.

В данном проекте используются такие запросы:
- GET
- POST 
- PATCH 
- PUT 
- DELETE

Работа выполнена с помощью библиотек Django и Django Rest Framework (*DRF*). Для обработки запросов к API применяются Вьюсеты (*viewset*), к каждому из них написаны Сериализаторы (*serializers*). Роутинг запросов реализован с помощью *DefaultRouter* - одного из инструментов DRF. Так же в проекте предусмотрена аутентификация по *JWT*-токену. Права доступа для различных видов запросов отличаются, например чтение постов разрешено всем, а изенение - только автору поста. Это все заслуга различных пермишенов (*permissions*). Для более удобного и гибкого поиска постов исползуется пагинация, основанная на классе *LimitOffsetPagination* и поисковый бэкенд *SearchFilter*.

# Как запустить проект:

Установить и настроить Docker, с помощью официальной документации:

https://docs.docker.com/

Клонировать репозиторий:

`git clone git@github.com:Enh404/yamdb_final.git`

Заполнить _.env-файл_:

```DB_ENGINE=   # указываем, что работаем с postgresql```

```DB_NAME=   # имя базы данных```

```POSTGRES_USER=   # логин для подключения к базе данных```

```POSTGRES_PASSWORD=   # пароль для подключения к БД (установите свой)```

```DB_HOST=   # название сервиса (контейнера)```

```DB_PORT=   # порт для подключения к БД```

```SECRET_KEY=   # находится в settings.py```

 Перейти в директорию с _docker-compose_:

`cd yamdb_final/infra`

Развернуть проект, запустив _docker-compose_:

`docker-compose up -d`

Выполнить миграции:

`docker-compose exec web python manage.py migrate`

Создать суперпользователя:

`docker-compose exec web python manage.py createsuperuser`

Собрать статику:

`docker-compose exec web python manage.py collectstatic --no-input`

Если потребуется остановить проект:

`docker-compose down -v`
