import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_daq as daq

class Gauge:
    def __init__(self, min, max, value, id, title, color='#1aad5a'):
        self.min=min
        self.max=max
        self.value=value
        self.id=id
        self.title=title
        self.color=color

    def generate(self):
        return dbc.Card(
            children=[
                dbc.CardHeader(
                    self.title,
                    style={
                        "text-align": "center",
                        "color": "white",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                        "border-top": "1px solid rgb(216, 216, 216)",
                    },
                ),
                dbc.CardBody(
                    [
                        html.Div(
                            daq.Gauge(
                                id=self.id,
                                min=self.min,
                                max=self.max,
                                value=self.value,
                                showCurrentValue=True,
                                color=self.color,
                                style={
                                    "align": "center",
                                    "display": "flex",
                                    "marginTop": "5%",
                                    "marginBottom": "-10%",
                                },
                            ),
                            className="m-auto",
                            style={
                                "display": "flex",
                                "backgroundColor": "black",
                                "border-radius": "1px",
                                "border-width": "5px",
                            },
                        )
                    ],
                    className="d-flex",
                    style={
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                        "border-top": "1px solid rgb(216, 216, 216)",
                    },
                ),
            ],
            style={"height": "95%"},
        )