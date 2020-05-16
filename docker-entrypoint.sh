#!/bin/bash


echo "======Собираем статику======"
echo "======Долго, грузим на S3======"
python manage.py collectstatic --noinput

echo "======Таки ждем, пока постгра поднимется======"
while ! curl http://web_db:5432/ 2>&1 | grep '52'
do
  echo "Таки ждем....."
  sleep 1
done
echo "Таки дождались..........."

echo "======Накатываем миграции======"
#python manage.py makemigrations
python manage.py migrate
# python manage.py loaddata dump_db.json # -> создать дамп чистой базы с конфигурацией allauth

echo "======Стартуем сервер======"
#python manage.py runserver 0.0.0.0:80
daphne -e ssl:443:privateKey=config/ssl/privkey.pem:certKey=config/ssl/fullchain.pem  -b 0.0.0.0 -p 80 Scanner.asgi:application
