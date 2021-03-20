import os
import warnings

import numpy as np
import pandas as pd
import progressbar

try:
    from mysql_connection import db_connect

except ModuleNotFoundError:
    from database.mysql_connection import db_connect


def merge_and_clean_data():
    if os.getcwd()[-5:] == 'yasap':
        os.chdir('database')

    season = pd.read_csv('new_data/season.csv')
    season.drop(columns=['W-L-T Home', 'W-L-T Away'], inplace=True)
    season['team'] = season['team'].str.upper()
    season['team'].replace({'KC': 'SKC'}, inplace=True)

    playoffs = pd.read_csv('new_data/playoffs.csv')
    playoffs.replace({'Yes': 1, 'No': 0}, inplace=True)
    playoffs['team'] = playoffs['team'].str.upper()
    playoffs['team'].replace({'KC': 'SKC'}, inplace=True)
    playoffs.drop(columns='teamName', inplace=True)  # Unreliable

    merged = pd.merge(left=season, right=playoffs, on=['season', 'team'],
                      how='outer', indicator=True)

    assert list(merged['_merge'].unique()) == ['both', 'left_only']
    merged.drop(columns='_merge', inplace=True)

    new_names = {
        'NY Red Bulls': 'New York Red Bulls',
        'Minnesota United FC': 'Minnesota United',
        'Atlanta United FC': 'Atlanta United',
        'Seattle Sounders FC': 'Seattle Sounders',
        'Vancouver Whitecaps FC': 'Vancouver Whitecaps FC',
        'Montreal Impact': 'CF Montreal'
    }

    merged.replace(new_names, inplace=True)

    for col in merged.columns:
        if merged[col].dtype == np.dtype('float64'):
            merged[col].fillna(0, inplace=True)
            merged[col] = merged[col].astype(int)

    return merged


def push_standings_data():
    df = merge_and_clean_data()

    cnxn = db_connect()
    cursor = cnxn.cursor()
    cursor.execute('use box2box')

    records = [tuple(x) for x in df.to_records(index=False)]

    for record in progressbar.progressbar(records):
        query = "INSERT INTO standings (season, ranking, team, teamName, points, gamesPlayed, wins, losses, ties, goalsFor, goalsAgainst, " \
                "playoffsGamesPlayed, playoffsWins, playoffsLosses, playoffsTies, playoffsGoalsFor, " \
                "playoffsGoalsAgainst, firstRound, secondRound, confFinal, mlsCup)" \
                f" VALUES {record}"

        cursor.execute(query)
        cnxn.commit()

    cnxn.close()


if __name__ == '__main__':

    warnings.simplefilter(action='ignore', category=FutureWarning)
    push_standings_data()
