#!/bin/bash

echo "🚀 Запуск проекта с Finch..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте его из .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

# Проверка статуса VM
if ! finch vm status | grep -q "Running"; then
    echo "Запуск Finch VM..."
    finch vm start
fi

# Остановка и удаление старых контейнеров
echo "Очистка старых контейнеров..."
finch compose down

# Пересборка и запуск контейнеров
echo "Сборка и запуск контейнеров..."
finch compose up -d --build

echo "✅ Проект запущен!"
echo ""
echo "🌐 Dagster UI: http://localhost:3000"
echo "🗄️  MinIO Console: http://localhost:9001"
echo ""
echo "Проверьте состояние: ./scripts/healthcheck.sh"
echo "Просмотр логов: ./scripts/logs.sh"
