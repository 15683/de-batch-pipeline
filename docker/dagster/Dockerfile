# Dockerfile с поддержкой uv
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Настройка рабочей директории
WORKDIR /opt/dagster/app

# Копируем файлы зависимостей
COPY requirements.txt .

# Установка зависимостей БЕЗ виртуального окружения (флаг --system)
# В Docker контейнере виртуальное окружение не нужно!
RUN uv pip install --system --no-cache -r requirements.txt

# Копируем код приложения
COPY . .

# Настройка Dagster
ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV PYTHONPATH=/opt/dagster/app
ENV DAGSTER_MODULE_NAME=main

RUN mkdir -p $DAGSTER_HOME

# Копируем dagster.yaml в DAGSTER_HOME
COPY dagster_home/dagster.yaml $DAGSTER_HOME/

EXPOSE 3000

CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-m", "main"]
