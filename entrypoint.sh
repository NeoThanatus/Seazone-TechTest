#!/bin/sh

until nc -z -v -w30 db 5432
 do
   echo "waiting the database initialization..."
   sleep 3
 done

echo "database available, running migrations..."

alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
