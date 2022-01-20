import database_manager
from datetime import date
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go

dbm = database_manager.DatabaseManager()

def generate():
    data = dbm.query('intraday', 'distance', period='15min')['activities-distance-intraday']['dataset']

    half_hourly_x = []
    half_hourly_y = []
    for i in range(0, len(data), 2):
        half_hourly_x.append(data[i]['time'])
        if i+1 == len(data):
            half_hourly_y.append(data[i]['value'])
            break
        half_hourly_y.append(data[i]['value']+data[i+1]['value'])

    cumulative_x = []
    cumulative_y = []
    total = 0
    for d in data:
        total = total + d['value']
        cumulative_x.append(d['time'])
        cumulative_y.append(total)

    fig = px.line(
        x=cumulative_x,
        y=cumulative_y,
        labels=dict(x="Time", y="Distance")
    )

    fig.add_bar(
        x=half_hourly_x,
        y=half_hourly_y
    )

    return html.Div(
        dcc.Graph(figure=fig)
    )