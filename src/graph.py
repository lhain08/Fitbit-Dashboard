import dash
from dash import dcc
from dash import html
import plotly.express as px
import datetime

class Graph:
    def __init__(self, x, xaxis, y, yaxis, avg):
        self.x=x
        self.xaxis=xaxis
        self.y=y
        self.yaxis=yaxis
        self.avg=avg

    def generate(self):
        fig = px.scatter(x=self.x,
                         y=self.y,
                         trendline="rolling",
                         labels={
                             "x":self.xaxis,
                             "y":self.yaxis
                         },
                         trendline_options=dict(window=30))
        fig.data = [t for t in fig.data if t.mode == "lines"]

        fig.update_xaxes(range=[datetime.datetime.now() - datetime.timedelta(days=365),
                                datetime.datetime.now()])
        fig.update_yaxes(fixedrange=True)

        fig.update_layout(modebar_remove=['zoom', 'zoomIn', 'zoomOut'],
                          dragmode='pan')

        return html.Div(
            dcc.Graph(figure=fig)
        )