#!/bin/ash

echo "Apply migrations"

cd ./message_client
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

exec"$@"