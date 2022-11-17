#!/bin/sh
echo "CHECKING DATABASE CONNECTION"
while true; do sleep 5 && python db_connection_test.py && break; done
echo "DATABASE CONNECTION IS UP"

flask db upgrade

service nginx restart
cat /var/log/nginx/error.log

gunicorn -b 127.0.0.1:8080 --workers 4 --preload app:app
