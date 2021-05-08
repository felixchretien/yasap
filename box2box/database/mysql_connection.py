import os
import dotenv
import mysql.connector
import pandas as pd


def db_connect():

    dotenv.load_dotenv()

    config = {
        'user': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'host': os.getenv('IP'),
    }

    return mysql.connector.connect(**config)


def execute_query(query):

    cnxn = db_connect()
    cursor = cnxn.cursor()
    cursor.execute(query)
    out_df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    cnxn.close()

    return out_df


def create_compensation_table():

    if os.getcwd()[-5:] == 'yasap':
        os.chdir('database')

    with open("create_compensation_table.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    cnxn = db_connect()

    cursor = cnxn.cursor()

    cursor.execute('USE box2box')
    cursor.execute(query)

    cnxn.commit()
    cnxn.close()


def create_standings_table():

    if os.getcwd()[-5:] == 'yasap':
        os.chdir('database')

    with open("create_standings_table.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    cnxn = db_connect()

    cursor = cnxn.cursor()

    cursor.execute('USE box2box')
    cursor.execute(query)

    cnxn.commit()
    cnxn.close()
