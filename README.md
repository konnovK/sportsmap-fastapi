# sportsmap API


Python aiohttp бэкенд сервер для сайта __sportsmap.spb.ru__
для хранения и обработки данных пользователей и 
спортивных объектов.


## API Docs


Используется Swagger: [Документация API](https://sportsmap.spb.ru/new-api/docs).

После запуска сервера документацию swagger можно найти по url: `/`.

## Системные требования


- __Python__ версии 3.10 и новее
- __Docker__ 


## Миграции

Используется alembic. Скрипт `db/__main__.py` управляет миграциями:

- `python db --db-url <DB_URL> upgrade head` - применить миграции

- `python db --db-url <DB_URL> revision --message="<DESCRIPTION>" --autogenerate` - сгенерировать миграции

## Деплой


Используется __Docker__. Для запуска требуется передать
переменные окружения.

Например (для запуска сервера на порту 8080):

`docker build --tag=sportsmap-backend .`

`docker run -e API_DB_URL=postgresql://user:password@host:port/db -e API_SUPERUSER_EMAIL=superuser@example.com -e API_SUPERUSER_PASSWORD=hackme --detach --restart always sportsmap-backend`

При использовании __Docker Compose__:

`docker build --build-arg API_PORT=8080 --tag=sportsmap-backend .`

```
backend:
    image: sportsmap-backend
    expose:
      - 8080
    environment:
      - API_DB_URL=postgresql://user:password@host:port/db
      - API_SUPERUSER_EMAIL=superuser@example.com
      - API_SUPERUSER_PASSWORD=hackme
```

### Список переменных окружения:

Управление настройками и окружением находится в скрипте `settings/settings.py`.

- `API_HOST` - хост сервера _(опционально)_
- `API_PORT` - порт сервера _(опционально)_
- `API_DB_URL` - адрес базы данных (см. [sqlalchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls))
- `API_TEST_DB_URL` - адрес базы данных, используемой для тестов (см. [sqlalchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls))
- `API_DB_USE_SSL` - передать, если нужно использовать ssl сертификат при подключении к бд _(опционально)_
- `API_SUPERUSER_EMAIL` - email пользователя с правами администратора
- `API_SUPERUSER_PASSWORD` - пароль пользоватля с правами администратора
- `YANDEX_GEOCODER_API_KEY` - ключ доступа для API яндекс геокодера (см. [API Геокодера](https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html?from=mapsapi))
- `YANDEX_OBJECT_STORAGE_KEY_ID` - ID ключа доступа для Yandex Object Storage (см. [Yandex Cloud Docs](https://cloud.yandex.ru/docs/iam/operations/sa/create-access-key))
- `YANDEX_OBJECT_STORAGE_ACCESS_KEY` - ключ доступа для Yandex Object Storage (см. [Yandex Cloud Docs](https://cloud.yandex.ru/docs/iam/operations/sa/create-access-key))
- `SMTP_HOST` - Хост SMTP сервера для работы с почтой
- `SMTP_USER` - Админский email
- `SMTP_PASSWORD` - Пароль smtp приложений для админского email
- `API_DEBUG` - debug режим
- `YANDEX_CLOUD_LOGGING_OAUTH` - ключ для работы с Yandex Cloud Logging (см. [Yandex Cloud Logging Docs](https://cloud.yandex.ru/docs/logging/))
- `YANDEX_CLOUD_LOGGING_LOG_GROUP_ID` - группа логов в Yandex Cloud Logging (см. [Yandex Cloud Logging Docs](https://cloud.yandex.ru/docs/logging/))


## Дополнительные материалы


- __Yandex geocoder API__ - https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html?from=mapsapi
- __Yandex Object storage__ - https://cloud.yandex.ru/docs/storage/
- __Yandex Cloud Logging__ - https://cloud.yandex.ru/docs/logging/
---

`aiohttp` `SQLAlchemy` `asyncpg` `alembic` `boto3` `pytest` `pandas` `pyjwt` `marshmallow` `FastAPI`