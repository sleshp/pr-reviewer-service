PYTHON := python
PIP := $(PYTHON) -m pip

VENV_DIR := .venv
ACTIVATE := . $(VENV_DIR)/bin/activate

.PHONY: help venv install run run-dev lint fmt test alembic-up alembic-downgrade docker-up docker-down docker-rebuild

help:
	@echo "Доступные команды:"
	@echo "  make venv            - создать виртуальное окружение (.venv)"
	@echo "  make install         - установить зависимости в .venv"
	@echo "  make run-dev         - запустить FastAPI локально (uvicorn, порт 8080)"
	@echo "  make alembic-up      - применить миграции (alembic upgrade head)"
	@echo "  make alembic-downgrade REV=... - откатить миграции до ревизии"
	@echo "  make lint            - запустить black и isort в режиме проверки"
	@echo "  make fmt             - автоформатирование black + isort"
	@echo "  make docker-up       - запустить сервис и БД через docker compose"
	@echo "  make docker-down     - остановить docker compose и удалить контейнеры"
	@echo "  make docker-rebuild  - пересобрать образы и запустить заново"

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(ACTIVATE) && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt

run-dev:
	$(ACTIVATE) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

alembic-up:
	$(ACTIVATE) && alembic upgrade head

alembic-downgrade:
	$(ACTIVATE) && alembic downgrade $(REV)

lint:
	$(ACTIVATE) && black --check app alembic
	$(ACTIVATE) && isort --check-only app alembic

fmt:
	$(ACTIVATE) && isort app alembic
	$(ACTIVATE) && black app alembic

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-rebuild:
	docker compose down
	docker compose up --build
