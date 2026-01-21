#!/bin/bash

echo "Остановка контейнеров..."
finch compose -f docker-compose.yaml down

echo "Проект остановлен"
