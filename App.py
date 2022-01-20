import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import datetime

import database_manager
import gauge
import graph
import today

DBManager = database_manager.DatabaseManager()
today_date = datetime.date.today()
start_date = today_date - datetime.timedelta(days=365) # datetime.date(today.year, 1, 1)
data = DBManager.query('time_series', 'distance', start_date, today_date)
values = []
dates = []
for d in data:
    values.append(float(d['value']))
    dates.append(pd.to_datetime(d["dateTime"], format="%Y-%m-%d"))
avg = sum(values)/len(values)
dates_passed = datetime.date.today() - datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
dates_passed = dates_passed.days + 1
dates_to_go = datetime.datetime.strptime("2022-12-31", "%Y-%m-%d").date() - datetime.date.today()
dates_to_go = dates_to_go.days

gauge_color = {
    'gradient':True,
    'ranges': {
        'red':[0,1.5],
        'yellow':[1.5,3],
        'green':[3,5]
    }
}

dist_graph = graph.Graph(dates, "Date", values, "Distance as Rolling 30-Day Mean", avg)
avg_gauge = gauge.Gauge(0, 5, avg, 'avg-gauge', 'Average VS Goal', color=gauge_color)
to_go_gauge = gauge.Gauge(0, 20, ((dates_passed + dates_to_go) * 4.25 - avg * dates_passed) / dates_to_go, 'to-go-gauge', 'Needed Remaining Average')
app = dash.Dash(__name__)

selected_tab_style = {
    'fontWeight': 'bold',
    'color': 'green',
    'borderTop': '3px solid darkgreen'
}
tab_style = {
    'color': 'green'
}

app.layout=html.Div([
    dcc.Tabs([
        dcc.Tab(label='Today', selected_style=selected_tab_style, style=tab_style, children=[
            today.generate()
        ]),
        dcc.Tab(label='Experimental', selected_style=selected_tab_style, style=tab_style, children=[
            html.Div(dist_graph.generate()),
            html.Div(avg_gauge.generate(),
                     style={"float":"left"}),
            html.Div(to_go_gauge.generate(),
                     style={"float":"left"}),
            html.Div(
                dcc.Slider(
                    id='goal-slider',
                    min=0,
                    max=10,
                    step=0.1,
                    value=4.25,
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                style={"float":"left", "width":"25%"}
            ),
        ])
    ])
])
app.title = "Fitbit Dashboard"

@app.callback(
    dash.dependencies.Output('to-go-gauge', 'value'),
    [dash.dependencies.Input('goal-slider', 'value')])
def update_output(value):
    print(((dates_passed + dates_to_go) * value - avg * dates_passed) / dates_to_go)
    return ((dates_passed + dates_to_go) * value - avg * dates_passed) / dates_to_go

if __name__ == "__main__":
    app.run_server(debug=True)