#!/bin/bash

# Скрипт для установки локального окружения
echo "Настройка локального окружения разработки..."

# Создание .env файла если его нет
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Создан .env файл из .env.example"
fi

# Установка зависимостей с помощью uv
echo "Установка зависимостей..."
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

echo "✅ Локальное окружение готово!"
echo "Активируйте окружение: source .venv/bin/activate"
