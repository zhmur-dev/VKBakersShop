from os import getenv
from pathlib import Path

import psycopg2
from dotenv.main import load_dotenv

import ui

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

database = getenv('DATABASE_NAME', 'db')
psycopg_config = {
    'user': getenv('POSTGRES_USER', 'postgres'),
    'password': getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': getenv('DB_HOST', 'localhost'),
    'port': getenv('DB_PORT', '5432'),
}


def create_db():
    try:
        print(ui.CREATING_DB)
        conn = psycopg2.connect(database='postgres', **psycopg_config)
        conn.autocommit = True
        conn.cursor().execute('CREATE database ' + database + ';')
        print(ui.DB_CREATED)
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def populate_db():
    try:
        print(ui.POPULATING_DB)
        conn = psycopg2.connect(database=database, **psycopg_config)
        conn.autocommit = True
        with open(BASE_DIR / 'backend/sample_db/sql', 'r') as file:
            conn.cursor().execute(file.read())
        print(ui.DB_POPULATED)
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def delete_db():
    try:
        print(ui.DELETING_DB)
        conn = psycopg2.connect(database='postgres', **psycopg_config)
        conn.autocommit = True
        conn.cursor().execute('DROP database ' + database + ';')
        print(ui.DB_DELETED)
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_categories():
    try:
        with psycopg2.connect(database=database, **psycopg_config) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM category;')
                return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_category_name(category_id):
    try:
        with psycopg2.connect(database=database, **psycopg_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT name FROM category WHERE id = '
                    + str(category_id) + ';'
                )
                return cur.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_products(category_id):
    try:
        with psycopg2.connect(database=database, **psycopg_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT * FROM product WHERE category_id = '
                    + str(category_id) + ';'
                )
                return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_product_details(product_id):
    try:
        with psycopg2.connect(database=database, **psycopg_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT * FROM product WHERE id = ' + str(product_id) + ';'
                )
                return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
