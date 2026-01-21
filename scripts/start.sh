#!/bin/bash

echo "Запуск проекта с Finch..."

# Проверка статуса VM
if ! finch vm status | grep -q "Running"; then
    echo "Запуск Finch VM..."
    finch vm start
fi

# Запуск контейнеров
finch compose -f docker-compose.yaml up -d

echo "Проект запущен!"
echo "Dagster UI: http://localhost:3000"
echo "MinIO Console: http://localhost:9001"
