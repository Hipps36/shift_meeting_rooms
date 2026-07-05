# shift_meeting_rooms
Веб-сервис для автоматизации бронирования переговорных комнат в коворкинге. В системе есть несколько комнат, каждая из которых имеет заранее заданные временные слоты

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Hipps36/shift_meeting_rooms.git
```

```
cd shift_meeting_rooms
```

Cоздать и активировать виртуальное окружение:

```
python3.11 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости:

```
poetry install
```

Собрать docker обзазы и запустить контейнеры:

```
docker compose up
```

Данные для входа:
```
login: superuser@example.com
password: superuser
```

# Примеры использования
## Переговорные комнаты

/meeting_rooms/ GET - Получение всех переговорных комнат (Только для авторизованных пользователей)
```
Вывод:
[
  {
    "name": "string",
    "description": "string",
    "id": 0
  },
]
```

/meeting_rooms/ POST - Создание переговорной комнаты (Только для суперюзеров)
```
Ввод:
{
  "name": "string",
  "description": "string"
}

Вывод:
{
  "name": "string",
  "description": "string",
  "id": 0
}
```

/meeting_rooms/1/reservations/ DEL - Удаление переговорной комнаты (Только для суперюзеров)
```
Вывод:
{
  "name": "string",
  "description": "string",
  "id": 0
}
```

/meeting_rooms/1/reservations/ PATCH - Чатичное обновление переговорной комнаты (Только для суперюзеров)
```
Ввод:
{
  "name": "string",
  "description": "string"
}

Вывод:
{
  "name": "string",
  "description": "string",
  "id": 0
}
```

/meeting_rooms/1/reservations/ GET - Получение бронированей для переговорной комнаты (Только для суперюзеров)
```
Вывод:
[
  {
    "from_reserve": "2026-07-05T10:00",
    "to_reserve": "2026-07-05T11:00",
    "id": 0,
    "meetingroom_id": 0,
    "user_id": 0
  }
]
```

/meeting_rooms/1/available-slots?date_reserve=2026-07-01/ GET - Получние всех свободных временных отрезков переговорной комнаты на определенную дату (Только для авторизованных пользователей)
```
Вывод:
[
  {
    "start": "2026-07-01T00:00:00",
    "end": "2026-07-02T00:00:00"
  }
]
```

## Бронирования

/reservations/ GET - Получение всех броней (Только для суперюзеров)
```
Вывод:
[
  {
    "from_reserve": "2026-07-05T10:00",
    "to_reserve": "2026-07-05T11:00",
    "id": 0,
    "meetingroom_id": 0,
    "user_id": 0
  }
]
```

/reservations/ POST - Создание бронирования (Только для авторизованных пользователей)
```
Ввод:
{
  "from_reserve": "2026-07-05T10:00",
  "to_reserve": "2026-07-05T11:00",
  "meetingroom_id": 0
}

Вывод:
{
  "from_reserve": "2026-07-05T10:00",
  "to_reserve": "2026-07-05T11:00",
  "id": 0,
  "meetingroom_id": 0,
  "user_id": 0
}
```

/reservations/1/ DEL - Удаление бронирования (Для суперюзеров или создателей объекта бронирования)
```
Вывод:
{
  "from_reserve": "2026-07-05T10:00",
  "to_reserve": "2026-07-05T11:00",
  "id": 0,
  "meetingroom_id": 0,
  "user_id": 0
}
```

/reservations/1/ PATCH - Частичное обновление бронирования (Для суперюзеров или создателей объекта бронирования)
```
Ввод:
{
  "from_reserve": "2026-07-05T10:00",
  "to_reserve": "2026-07-05T11:00"
}

Вывод:
{
  "from_reserve": "2026-07-05T10:00",
  "to_reserve": "2026-07-05T11:00",
  "id": 0,
  "meetingroom_id": 0,
  "user_id": 0
}
```

/reservations/my_reservations/ GET - Получение списока всех бронирований для текущего пользователя (Только для авторизованных пользователей)
```
Вывод:
[
  {
    "from_reserve": "2026-07-05T10:00",
    "to_reserve": "2026-07-05T11:00",
    "id": 0,
    "meetingroom_id": 0,
    "user_id": 0
  }
]
```

## Авторизация

/auth/jwt/login/ POST - Логин
```
Ввод:
{
  "username": "user@example.com",
  "password": "string"
}

Вывод:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
  "token_type": "bearer"
}
```

/auth/jwt/logout/ POST - Логаут
```
Нет вывода
```

/auth/jwt/register/ POST - Регистрация (Только для суперюзеров)
```
Ввод:
{
  "email": "user@example.com",
  "password": "string"
}

Вывод:
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

## Пользователи

/user/me/ GET - Вывод текущего пользователя
```
Вывод:
{
  "id": 0,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

/user/me/ PATCH - Обновление текущего пользователя
```
Ввод:
{
  "email": "user@example.com",
  "password": "string"
}

Вывод:
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

/user/1/ GET - Вывод пользователя
```
Вывод:
{
  "id": 0,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

/user/1/ PATCH - Обновление пользователя
```
Ввод:
{
  "email": "user@example.com",
  "password": "string"
}

Вывод:
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

# Используемый стэк
Для разработки сервиса shift_meeting_rooms использовался следующий стэк:

Python FastAPI SQLAlchemy PostgreSQL

Документация:
[Swagger](http://127.0.0.1:8000/docs)
[ReDoc](http://127.0.0.1:8000/redoc/)

Автор проекта: [Максим Шашков](https://github.com/Hipps36)
