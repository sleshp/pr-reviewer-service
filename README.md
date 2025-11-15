# PR Reviewer Assignment Service

Сервис назначения ревьюверов для Pull Request’ов
(тестовое задание, осенняя волна 2025)

## Возможности сервиса

Сервис позволяет:

* управлять командами и их участниками;
* создавать Pull Request’ы и автоматически назначать до двух активных ревьюверов из команды автора;
* выполнять переназначение ревьюверов;
* получать список PR, назначенных конкретному пользователю.

API сервиса полностью описан в файле **openapi.yaml** и доступен по адресу:

```
http://localhost:8080/docs
```

---

## Технологический стек

* **Python 3.11**
* **FastAPI**
* **SQLAlchemy (async)**
* **PostgreSQL 16**
* **asyncpg**
* **Alembic** — миграции
* **Docker / Docker Compose**

---

## Запуск через Docker (рекомендуется)

Требуется установленный Docker и Docker Compose.

### Запуск

```bash
make docker-up
```

При запуске:

* поднимается PostgreSQL;
* применяются Alembic-миграции;
* стартует FastAPI на порту **8080**.

### Остановка

```bash
make docker-down
```

После запуска приложение доступно по адресу:

```
http://localhost:8080
```

---

## Локальный запуск без Docker

### 1. Установка зависимостей

```bash
make install
```

### 2. Убедиться, что в `.env` указан корректный `DATABASE_URL`

Пример для локального PostgreSQL:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pr_service
```

### 3. Применение миграций

```bash
make alembic-up
```

### 4. Запуск приложения

```bash
make run-dev
```

После запуска:

```
http://localhost:8080/docs
```

---
