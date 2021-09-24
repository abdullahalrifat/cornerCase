#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done
echo "Server Volume Mounted"

echo "file structure: "
ls

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done
echo "db connected"

python manage.py collectstatic --noinput

gunicorn cornerCase.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

#####################################################################################
# Options to DEBUG Django server
# Optional commands to replace above gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# DEBUG=True ./manage.py runserver 0.0.0.0:8000
