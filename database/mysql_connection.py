import os
import mysql.connector
import dotenv


def db_connect():

    dotenv.load_dotenv()

    config = {
        'user': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'host': os.getenv('IP'),
    }

    return mysql.connector.connect(**config)


def create_compensation_table():

    with open("database/create_compensation_table.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    cnxn = db_connect()

    cursor = cnxn.cursor()

    cursor.execute('USE box2box')
    cursor.execute(query)

    cnxn.close()
