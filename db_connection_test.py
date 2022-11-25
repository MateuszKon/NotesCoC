import os

import psycopg2
import libs.env_import  # Import for loading .env file before other imports


try:
    db = psycopg2.connect(
        database=os.environ.get("DATABASE_DB"),
        user=os.environ.get("DATABASE_USER"),
        host=os.environ.get("DATABASE_HOST"),
        password=os.environ.get("DATABASE_PASSWORD"),
    )
except:
    exit(1)
exit(0)
