#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Running migrations..."

python manage.py makemigrations --noinput
python manage.py makemigrations authentication --noinput
python manage.py makemigrations superadmin --noinput
python manage.py makemigrations vendor --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Migrated..."

python manage.py shell < create_user.py

exec "$@"