import os
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from box2box.analytics.plots.box2box_plots import scatter_plot_with_linreg_and_season_slider
from box2box.database.mysql_connection import db_connect

if os.getcwd()[-5:] == 'yasap':
    os.chdir('app/plots/utilite_des_dp')

if os.getcwd()[-5:] == 'plots':
    os.chdir('utilite_des_dp')


def plot_1():
    with open("utilite_des_dp_plot1.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    cnxn = db_connect()
    cursor = cnxn.cursor()
    cursor.execute(query)
    data = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    cnxn.close()

    coefs = dict()

    for i in ['goalsFor', 'goalsAgainst']:
        model = LinearRegression()
        model.fit(X=data[i].values.reshape(-1, 1), y=data['firstRound'])
        coefs[i] = round(abs(model.coef_[0]) * 100, 2)

    # Plot
    fig = go.Figure()

    fig.add_trace(go.Bar(y=['Buts contre  '],
                         x=[coefs['goalsAgainst']],
                         marker={'color': 'rgb(237,86,66)'},
                         orientation='h',
                         hovertemplate="Effet moyen: -%{x} %<br><extra></extra>"
                         ))

    fig.add_trace(go.Bar(y=['Buts pour  '],
                         x=[coefs['goalsFor']],
                         marker={'color': '#19af54'},
                         orientation='h',
                         hovertemplate="Effet moyen: %{x} %<br><extra></extra>"
                         ))

    fig.update_layout(yaxis_zeroline=False,
                      xaxis_zeroline=False,
                      paper_bgcolor='#eeeeee',
                      plot_bgcolor='#eeeeee',
                      font_color="black",
                      showlegend=False
                      )

    fig.write_html('plot1.html')


def plot_3():
    with open("utilite_des_dp_plot3.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    cnxn = db_connect()
    cursor = cnxn.cursor()
    cursor.execute(query)
    data = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    cnxn.close()

    data.dropna(inplace=True)  # Sporting Kansas City dont have the same team code (need to fix)
    data['totalCompensation'] = data['totalCompensation'].astype(int)

    fig = scatter_plot_with_linreg_and_season_slider(data=data, x_var='totalCompensation', y_var='goalsFor',
                                                     xlab='Dollars dépensés en attaque', ylab='Buts marqués')

    fig.write_html('plot3.html')


if __name__ == '__main__':
    plot_1()
    plot_3()
