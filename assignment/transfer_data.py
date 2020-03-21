import psycopg2
import datetime
from pymongo import MongoClient
from decimal import Decimal
from time import sleep


TABLES = [
    'actor',
    'address',
    'category',
    'city',
    'country',
    'customer',
    'film',
    'film_actor',
    'film_category',
    'inventory',
    'language',
    'payment',
    'rental',
    'staff',
    'store',
]
TYPE_HANDLERS = {
    datetime.date: lambda f: datetime.datetime.combine(f, datetime.time()),
    memoryview: lambda f: f.tobytes(),
    Decimal: lambda f: float(f)
}


def create_dbs():
    def get_postgres():
        while True:
            try:
                return psycopg2.connect(dbname='dvdrental', host='postgres',
                                        user='postgres', password='postgres')
            except Exception as e:
                print(f"Error: {e}", flush=True)
                sleep(1)

    client = MongoClient("mongodb://mongo")
    client.drop_database('dvdrental')
    return client['dvdrental'], get_postgres()


def transfer(mongo, postgres):
    for table in TABLES:
        cursor = postgres.cursor()
        cursor.execute(f'SELECT * FROM {table}')

        columns = [desc[0] for desc in cursor.description]
        table_data = cursor.fetchall()

        mongo[table].insert_many([
            {
                c: TYPE_HANDLERS[type(r)](r) if type(r) in TYPE_HANDLERS else r
                for c, r in zip(columns, row)
            } for row in table_data
        ])

        nrecords = mongo[table].count_documents({})
        print(f'Table "{table}": {nrecords} records inserted')
