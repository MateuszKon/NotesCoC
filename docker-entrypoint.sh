#!/bin/sh
#echo "CHECKING DATABASE CONNECTION"
#while true; do sleep 5 && python db_connection_test.py && break; done
#echo "DATABASE CONNECTION IS UP"

echo "FLASK DB UPGRADE START"
flask db upgrade
echo "FLASK DB UPGRADE FINISHED"

cd /app
echo "STARTING APP"
gunicorn -b 0.0.0.0:8000 --workers 2 --preload app:app
