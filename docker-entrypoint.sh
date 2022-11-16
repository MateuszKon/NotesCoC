#!/bin/sh

flask db upgrade

service nginx restart
cat /var/log/nginx/error.log

gunicorn -b 127.0.0.1:8080 --workers 4 --preload app:app
