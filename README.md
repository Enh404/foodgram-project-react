![example workflow](https://github.com/Enh404/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Описание проекта:

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Запуск проекта:

Установить и настроить Docker, с помощью официальной документации:

https://docs.docker.com/

Клонировать репозиторий:

`git clone git@github.com:Enh404/foodgram-project-react.git`

Заполнить _.env-файл_:

```DB_ENGINE=   # указываем, что работаем с postgresql```

```DB_NAME=   # имя базы данных```

```POSTGRES_USER=   # логин для подключения к базе данных```

```POSTGRES_PASSWORD=   # пароль для подключения к БД (установите свой)```

```DB_HOST=   # название сервиса (контейнера)```

```DB_PORT=   # порт для подключения к БД```

```SECRET_KEY=   # находится в settings.py```

 Перейти в директорию с _docker-compose_:

`cd foodgram-project-react/infra`

Развернуть проект, запустив _docker-compose_:

`docker-compose up -d`

Выполнить миграции:

`docker-compose exec backend python manage.py migrate`

Создать суперпользователя:

`docker-compose exec backend python manage.py createsuperuser`

Собрать статику:

`docker-compose exec backend python manage.py collectstatic --no-input`

Если потребуется остановить проект:

`docker-compose down -v`
