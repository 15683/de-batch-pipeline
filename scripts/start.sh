#!/bin/bash

echo "🚀 Запуск проекта с Finch..."

# Проверка статуса VM
if ! finch vm status | grep -q "Running"; then
    echo "Запуск Finch VM..."
    finch vm start
fi

# Остановка и удаление старых контейнеров
echo "Очистка старых контейнеров..."
finch compose down

# Пересборка и запуск контейнеров
echo "Запуск контейнеров..."
finch compose up -d

echo "✅ Проект запущен!"
echo ""
echo "🌐 Dagster UI: http://localhost:3000"
echo "🗄️  MinIO Console: http://localhost:9001"
echo ""
