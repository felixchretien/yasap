import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def scatter_plot_with_linreg_and_season_slider(data, x_var, y_var, xlab, ylab):
    fig = go.Figure()

    # One trace by season (for the slider)
    for season in data.season.unique():
        fig.add_trace(go.Scatter(
            visible=False,
            x=data.loc[data['season'] == season, x_var],
            y=data.loc[data['season'] == season, y_var],
            name='',
            mode='markers',
            marker={'color': '#19af54'},
            text=data.loc[data['season'] == season, 'teamName'],
            showlegend=False,
            hovertemplate="<b>%{text}</b><br><br>"
            f"{xlab}: " + "%{x:$,.0f}<br>"
            f"{ylab}: " + "%{y}<br>"
            "<extra></extra>"
        ))

        # Linear fit
        X = data.loc[data['season'] == season, x_var].values.reshape(-1, 1)
        y = data.loc[data['season'] == season, y_var].values

        model = LinearRegression()
        model.fit(X, y)

        x_range = np.linspace(X.min(), X.max(), 100)
        y_range = model.predict(x_range.reshape(-1, 1))

        fig.add_traces(go.Scatter(visible=False,
                                  x=x_range,
                                  y=y_range,
                                  name='',
                                  showlegend=False,
                                  marker={'color': '#19af54'},
                                  hovertemplate="Régression linéaire pour la saison"))

    fig.update_layout(yaxis_zeroline=False,
                      xaxis_zeroline=False,
                      paper_bgcolor='#eeeeee',
                      plot_bgcolor='#eeeeee',
                      xaxis_title=xlab,
                      yaxis_title=ylab,
                      font_color="black"
                      )

    fig.data[-1].visible = True
    fig.data[-2].visible = True

    # Create and add slider
    steps = []
    for i in range(int(len(fig.data) / 2)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],  # layout attribute
        )
        step["args"][0]["visible"][int(i * 2)] = True  # Toggle i*2'th trace to "visible"
        step["args"][0]["visible"][int(i * 2) + 1] = True  # Toggle i'th trace to "visible" (linear fit)
        steps.append(step)

    sliders = [dict(
        active=len(fig.data) - 1,
        currentvalue={"prefix": "Saison: ", 'font': {'size': 14}},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
    )

    for i, date in enumerate(data['season'].unique(), start=0):
        fig['layout']['sliders'][0]['steps'][i]['label'] = str(date)

    fig.layout.sliders[0].transition.duration = 100

    return fig


def team_time_series_plot(data, y_var, y_lab, highlight_teams, ratio=False):
    if not y_lab:
        y_lab = y_var

    fig = go.Figure()

    fig.update_layout(yaxis_zeroline=False,
                      xaxis_zeroline=False,
                      xaxis={'tickvals': list(data['season'].unique())},
                      xaxis_title='Saison',
                      yaxis_title=y_lab,
                      paper_bgcolor='#eeeeee',
                      plot_bgcolor='#eeeeee',
                      font_color="black",
                      margin=dict(pad=20)
                      )

    for team in data['team'].unique():

        if team in highlight_teams.keys():
            continue

        x = data.loc[data['team'] == team, 'season']
        y = data.loc[data['team'] == team, y_var]

        fig.add_trace(

            go.Scatter(x=x, y=y,
                       mode='lines',
                       line=dict(color='lightgrey'),
                       showlegend=False,
                       hovertemplate=f"{team}<br><br>"
                                     f"Saison: " + "%{x}<br>"
                                                   f"{y_lab}: " + f"{'%{y} %' if ratio else '%{y:.2f}'}<br>"
                                                                "<extra></extra>"
                       )
        )

    for team, color in highlight_teams.items():

        x = data.loc[data['team'] == team, 'season']
        y = data.loc[data['team'] == team, y_var]

        fig.add_trace(

            go.Scatter(x=x,
                       y=y,
                       mode='lines',
                       name=team,
                       line=dict(color=color, width=4),
                       hovertemplate=f"{team}<br>"
                                     f"Saison: " + "%{x}<br>"
                                                   f"{y_lab}: " + f"{'%{y} %' if ratio else '%{y:.2f}'}<br>"
                                                                "<extra></extra>"
                       )
        )

    return fig
