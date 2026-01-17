FROM python:3.11-slim

# Установка системных зависимостей (git нужен для dbt)
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dagster/app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python пакеты (используем кэш для ускорения)
RUN pip install --no-cache-dir -r requirements.txt

# Настройка переменных окружения для Dagster
ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME

# Копируем конфиг дагстера (создадим его позже)
COPY orchestration/dagster.yaml $DAGSTER_HOME/

WORKDIR /workspaces/de-batch-pipeline
