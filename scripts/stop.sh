#!/bin/bash

echo "Остановка контейнеров..."
finch compose down -v

echo "Проект остановлен"
