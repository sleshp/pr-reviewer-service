PYTHON := python
PIP := pip

.PHONY: help venv install run run-dev lint fmt test

help:
	@echo "Доступные команды:"
	@echo "  make venv    - создать виртуальное окружение"
	@echo "  make install - установить зависимости"
	@echo "  make run-dev - запустить сервер"
	@echo "  make fmt     - автоформатирование"
	@echo "  make test    - запустить тесты"

venv:
	$(PYTHON) -m venv .venv

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run-dev:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

fmt:
	$(PYTHON) -m isort app alembic
	$(PYTHON) -m black app alembic

lint:
	$(PYTHON) -m black --check app alembic
	$(PYTHON) -m isort --check-only app alembic

test:
	$(PYTHON) -m pytest -q

alembic-up:
	$(PYTHON) -m alembic upgrade head

alembic-downgrade:
	$(PYTHON) -m alembic downgrade $(REV)

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-rebuild:
	docker compose down
	docker compose up --build