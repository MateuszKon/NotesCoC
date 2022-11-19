#!/usr/bin/python3
import logging
import subprocess

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def restore_postgres_db(db_host, db, port, user, password, backup_file, verbose):
    """
    Restore postgres db from a file.
    """

    if verbose:
        try:
            print(user,password,db_host,port, db)
            process = subprocess.Popen(
                ['pg_restore',
                 '--no-owner',
                 '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user,
                                                               password,
                                                               db_host,
                                                               port, db),
                 '-v',
                 backup_file],
                stdout=subprocess.PIPE
            )
            output = process.communicate()[0]
            if int(process.returncode) != 0:
                print('Command failed. Return code : {}'.format(process.returncode))

            return output
        except Exception as e:
            print("Issue with the db restore : {}".format(e))
    else:
        try:
            process = subprocess.Popen(
                ['pg_restore',
                 '--no-owner',
                 '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user,
                                                                      password,
                                                                      db_host,
                                                                      port, db),
                 backup_file],
                stdout=subprocess.PIPE
            )
            output = process.communicate()[0]
            if int(process.returncode) != 0:
                print('Command failed. Return code : {}'.format(process.returncode))

            return output
        except Exception as e:
            print("Issue with the db restore : {}".format(e))


def create_db(db_host, database, db_port, user_name, user_password):
    try:
        con = psycopg2.connect(dbname='postgres', port=db_port,
                               user=user_name, host=db_host,
                               password=user_password)

    except Exception as e:
        print(e)
        exit(1)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("DROP DATABASE {} ;".format(database))
    except Exception as e:
        print('DB does not exist, nothing to drop')
    cur.execute("CREATE DATABASE {} ;".format(database))
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE {} TO {} ;".format(database, user_name))
    return database


def swap_restore_active(db_host, restore_database, active_database, db_port, user_name, user_password):
    try:
        con = psycopg2.connect(dbname='postgres', port=db_port,
                               user=user_name, host=db_host,
                               password=user_password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute("SELECT pg_terminate_backend( pid ) "
                    "FROM pg_stat_activity "
                    "WHERE pid <> pg_backend_pid( ) "
                    "AND datname = '{}'".format(active_database))
        cur.execute("DROP DATABASE {}".format(active_database))
        cur.execute('ALTER DATABASE "{}" RENAME TO "{}";'.format(restore_database, active_database))
    except Exception as e:
        print(e)
        exit(1)


def main(
        postgres_host,
        postgres_port,
        postgres_db,
        postgres_user,
        postgres_password,
        restore_file,
):
    postgres_restore = "{}_restore".format(postgres_db),

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    # logger.info("Creating temp database for restore : {}".format(postgres_restore))
    # tmp_database = create_db(postgres_host,
    #           postgres_restore,
    #           postgres_port,
    #           postgres_user,
    #           postgres_password)
    # logger.info("Created temp database for restore : {}".format(tmp_database))
    # logger.info("Restore starting")
    result = restore_postgres_db(postgres_host,
                                 postgres_db,
                                 postgres_port,
                                 postgres_user,
                                 postgres_password,
                                 restore_file,
                                 True)
    for line in result.splitlines():
        logger.info(line)
    logger.info("Restore complete")

    # restored_db_name = postgres_db
    # logger.info("Switching restored database with active one : {} > {}".format(
    #     postgres_restore, restored_db_name
    # ))
    # swap_restore_active(postgres_host,
    #                     postgres_restore,
    #                     restored_db_name,
    #                     postgres_port,
    #                     postgres_user,
    #                     postgres_password)

    logger.info("Database restored and active.")


if __name__ == '__main__':
    main(
        postgres_host='',
        postgres_port='',
        postgres_db='',
        postgres_user='',
        postgres_password='',
        restore_file='',
    )
