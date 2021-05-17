import os
import plotly.graph_objects as go

from box2box.analytics.plots.box2box_plots import team_time_series_plot
from box2box.database.mysql_connection import execute_query

if os.getcwd()[-5:] == 'yasap':
    os.chdir('box2box/analytics/plots/bezbatchenko')

if os.getcwd()[-5:] == 'plots':
    os.chdir('bezbatchenko')


def old_plot():
    """Not used anymore"""

    with open("bezbatchenko_plot1.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    data = execute_query(query)

    for i in ['dp_total', 'total', 'dp_share']:
        data[i] = data[i].astype(int)

    fig = team_time_series_plot(data=data,
                                y_var='dp_share',
                                y_lab='Pourcentage',
                                ratio=True,
                                highlight_teams={'TOR': 'rgb(169,33,49)',
                                                 'CLB': 'rgb(255,241,54)',
                                                 'MTL': 'rgb(6, 55, 158)'})

    fig.write_html('plot1.html')


def plot_1():
    with open("bezbatchenko_plot1.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    data = execute_query(query)

    for i in ['dp_total', 'total', 'dp_share']:
        data[i] = data[i].astype(int)

    data['total'] = data['total'] / 1000000
    data['dp_total'] = data['dp_total'] / 1000000

    fig = team_time_series_plot(data=data,
                                y_var='dp_total',
                                y_lab='Total en millions USD',
                                ratio=False,
                                highlight_teams={'TOR': 'rgb(169,33,49)',
                                                 'CLB': 'rgb(255,241,54)',
                                                 'MTL': 'rgb(6, 55, 158)'})

    fig.write_html('../../../templates/plots/plot1.html')


def plot_2():
    with open("bezbatchenko_plot2.sql", 'r') as reader:
        query = reader.read().replace('\n', ' ')

    data = execute_query(query)

    data['Invitée aux séries'] = 0
    data.loc[data['firstRound'] == 1, 'Invitée aux séries'] = 1
    data.loc[data['secondRound'] == 1, 'Invitée aux séries'] = 1
    data.loc[data['confFinal'] == 1, 'Invitée aux séries'] = 1
    data.loc[data['mlsCup'] == 1, 'Invitée aux séries'] = 1

    data['Participation aux séries'] = 'Exclue des séries'
    data.loc[data['Invitée aux séries'] == 1, 'Participation aux séries'] = 'Invitée aux séries'

    fig = go.Figure()

    # Need to go through the rist loop before starting the second one!
    for i in ['Exclue des séries', 'Invitée aux séries']:
        fig.add_trace(go.Box(y=data.loc[data['Participation aux séries'] == i, "teamTotalCompensation"],
                             x=data.loc[data['Participation aux séries'] == i, "Participation aux séries"],
                             customdata=data[data['Participation aux séries'] == i],
                             whiskerwidth=0.2,
                             marker_size=4,
                             line_width=1,
                             pointpos=0,
                             fillcolor='rgba(255,255,255,0)',
                             boxpoints="all", boxmean=True, name='',
                             marker={'color': '#19af54'}, showlegend=False, line_color='rgba(111,111,111,0.4)',
                             hovertemplate='%{customdata[0]} '
                                           '%{customdata[1]}<br>'
                                           "%{y:$,.0f}<br>"
                                           "<extra></extra>"
                             ))

    fig.update_layout(yaxis_zeroline=False,
                      xaxis_zeroline=False,
                      paper_bgcolor='#eeeeee',
                      plot_bgcolor='#eeeeee',
                      font_color="black",
                      showlegend=False
                      )

    fig.write_html('../../../templates/plots/plot2.html')


if __name__ == '__main__':
    plot_1()
    plot_2()
