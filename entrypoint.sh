#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Creating superuser..."
python -m app.scripts.create_superuser

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
