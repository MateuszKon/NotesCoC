#!/bin/sh
echo "CHECKING DATABASE CONNECTION"
while true; do sleep 5 && python db_connection_test.py && break; done
echo "DATABASE CONNECTION IS UP"

flask db upgrade

cd /etc/nginx/
openssl req -x509 -sha256 -nodes -newkey rsa:2048 -days 365 -keyout localhost.key -out localhost.crt

service nginx restart
cat /var/log/nginx/error.log

cd /app
gunicorn -b 127.0.0.1:8080 --workers 4 --preload app:app
