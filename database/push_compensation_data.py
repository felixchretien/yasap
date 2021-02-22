import os
import warnings

import pandas as pd
import progressbar

try:
    from mysql_connection import db_connect

except ModuleNotFoundError:
    from database.mysql_connection import db_connect


def push_compensation_data():

    if os.getcwd()[-5:] == 'yasap':
        os.chdir('database')

    df = pd.read_csv('new_data/new_data.csv', sep=';')

    df['Total Compensation'] = df['Total Compensation'].str.replace(r"\xa0", "").astype(int)

    df['Base Salary'] = df['Base Salary'].str.replace(r"\xa0", "").astype(int)

    df.drop(columns='Unnamed: 8', inplace=True)

    df['DP'].replace({'DP': 1}, inplace=True)
    df['DP'].fillna(0, inplace=True)

    df.fillna('NULL', inplace=True)

    cnxn = db_connect()
    cursor = cnxn.cursor()
    cursor.execute('use box2box')

    records = [tuple(x) for x in df.to_records(index=False)]

    for record in progressbar.progressbar(records):
        query = "INSERT INTO compensation (season, club, firstName, lastName, position, " \
                "totalCompensation, baseSalary, dp)" \
                f" VALUES {record}"

        cursor.execute(query)
        cnxn.commit()

    cnxn.close()


if __name__ == '__main__':

    warnings.simplefilter(action='ignore', category=FutureWarning)
    push_compensation_data()
