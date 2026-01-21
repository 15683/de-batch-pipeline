#!/bin/bash

echo "Очистка неиспользуемых ресурсов..."
finch system prune -af
finch volume prune -f

echo "Очистка завершена"
