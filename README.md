# TODO API

Асинхронное REST API для управления задачами на **FastAPI** + **SQLAlchemy** + **PostgreSQL**.

## 🚀 Возможности

- ✅ Асинхронные CRUD операции
- ✅ SQLAlchemy 2.0 с async support
- ✅ PostgreSQL через Docker Compose
- ✅ Pydantic v2 для валидации
- ✅ Автоматическая документация (Swagger UI, ReDoc)

## 📋 Требования

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (пакетный менеджер)
- Docker & Docker Compose

## 🔧 Установка и запуск

### 1. Запуск через Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов (БД + API)
docker-compose up -d

# API доступен на http://localhost:8000
# Документация: http://localhost:8000/docs
```

### 2. Локальная разработка

```bash
# Установка зависимостей через uv
uv sync

# Запуск PostgreSQL (только БД)
docker-compose up -d db

# Запуск сервера разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/v1/todos` | Получить список задач |
| GET | `/api/v1/todos/{id}` | Получить задачу по ID |
| POST | `/api/v1/todos` | Создать новую задачу |
| PUT | `/api/v1/todos/{id}` | Обновить задачу |
| DELETE | `/api/v1/todos/{id}` | Удалить задачу |

### Примеры запросов

**Создать задачу:**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Изучить FastAPI", "description": "Создать TODO приложение"}'
```

**Получить все задачи:**
```bash
curl http://localhost:8000/api/v1/todos
```

**Отфильтровать по статусу:**
```bash
curl "http://localhost:8000/api/v1/todos?completed=false"
```

## 🗂️ Структура проекта

```
faproject/
├── app/
│   ├── core/          # Конфигурация, БД
│   ├── models/        # SQLAlchemy модели
│   ├── schemas/       # Pydantic схемы
│   ├── crud/          # CRUD операции
│   ├── routers/       # API роуты
│   └── main.py        # Точка входа
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── .env
```

## 🔐 Переменные окружения

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `POSTGRES_USER` | `postgres` | Пользователь БД |
| `POSTGRES_PASSWORD` | `postgres` | Пароль БД |
| `POSTGRES_DB` | `todo_db` | Имя БД |
| `DB_HOST` | `localhost` | Хост БД |
| `DB_PORT` | `5432` | Порт БД |

## 🧪 Тестирование

```bash
# Запуск тестов (когда будут добавлены)
pytest
```

## 📝 Лицензия

MIT
