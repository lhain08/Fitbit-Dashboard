import database_manager
from datetime import date
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

dbm = database_manager.DatabaseManager()

def generate():
    data = dbm.query('intraday', 'distance', period='15min')
    dataset = data['activities-distance-intraday']['dataset']
    datatotal = data['activities-distance'][0]

    distance_fig = make_distance_chart(dataset)

    return html.Div(children=[
        dbc.Card(
            dcc.Graph(figure=distance_fig, config={'displayModeBar':False}, style={
                    'padding':'1%'
                }),
            color='primary',
            outline='True',
            style={
                'float':'left',
                'margin':'auto',
                'width':'75%'
            }
        ),
        make_goal_card(datatotal, style={
            'float':'left',
            'margin':'auto',
            'width':'24%',
        })
    ])

def make_distance_chart(data):
    # Clumps data into half hour blocks
    half_hourly_x = []
    half_hourly_y = []
    for i in range(0, len(data), 2):
        half_hourly_x.append(data[i]['time'])
        if i+1 == len(data):
            half_hourly_y.append(data[i]['value'])
            break
        half_hourly_y.append(data[i]['value']+data[i+1]['value'])

    # Gets cumulative distance for each time stamp so far in the day
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

    fig.update_layout(modebar_remove=['zoom', 'zoomIn', 'zoomOut', 'boxSelect'],
                      dragmode='pan')

    return fig

def make_goal_card(data, style={}):
    dist = float(data['value'])
    return dbc.Card(
        dbc.ListGroup(
            [
                dbc.ListGroupItem([
                    html.H4("Total Distance", className="card-title"),
                    html.H2("{:.2f}".format(dist), style={
                        'text-align':'center'
                    })
                ]),
                dbc.ListGroupItem([
                    html.H4("Distance to Goal", className="card-title"),
                    html.H2("{:.2f}".format(4-dist), style={
                        'text-align':'center'
                    })
                ])
            ],
            flush=True
        ),
        style=style,
        color='primary',
        outline=True,
    )