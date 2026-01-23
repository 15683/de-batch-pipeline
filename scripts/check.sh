#!/bin/bash

echo "🔍 Проверка состояния сервисов..."

# Проверка PostgreSQL
echo -n "PostgreSQL: "
if finch exec de_pipeline_postgres pg_isready -U dagster > /dev/null 2>&1; then
    echo "✅ Работает"
else
    echo "❌ Не доступен"
fi

# Проверка MinIO
echo -n "MinIO: "
if curl -s http://localhost:9000/minio/health/live > /dev/null 2>&1; then
    echo "✅ Работает"
else
    echo "❌ Не доступен"
fi

# Проверка Dagster Webserver
echo -n "Dagster Webserver: "
if curl -s http://localhost:3000/server_info > /dev/null 2>&1; then
    echo "✅ Работает"
else
    echo "❌ Не доступен"
    echo "Проверьте логи: finch logs de_pipeline_dagster_web"
fi

echo ""
echo "Все логи: ./scripts/logs.sh"
