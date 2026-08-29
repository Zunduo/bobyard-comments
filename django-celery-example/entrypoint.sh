#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for PostgreSQL..."
until nc -z "${POSTGRES_HOST:-postgres}" "${POSTGRES_PORT:-5432}"; do
  sleep 1
done

echo "Waiting for Redis..."
until nc -z "${REDIS_HOST:-redis}" "${REDIS_PORT:-6379}"; do
  sleep 1
done

python manage.py migrate --noinput

exec "$@"
