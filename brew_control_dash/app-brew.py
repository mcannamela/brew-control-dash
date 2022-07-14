import datetime
import pytz
from collections import deque

import numpy as np
import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output
from brew_control_client.brew_state import BrewState

from brew_control_client import BrewControlClient

# pip install pyorbital
from brew_control_dash.brew_control_client_dash import get_client_factory
from brew_control_dash.plot_brew import plot_brew_state

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Brew Control'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )
    ])
)

time = deque(maxlen=20)
time_offset = (datetime.datetime.now(tz=pytz.UTC)-datetime.datetime(1970, 1, 1,tzinfo=pytz.UTC)).total_seconds()
time.append(0)
temperature = deque(maxlen=20)
temperature.append(0)
flow_rate = deque(maxlen=20)
flow_rate.append(0)



# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(input_data):
    factory = get_client_factory()

    test_temp = 30.0
    mashing_temp = 65.20
    strike_temp = 80.0
    mash_out_temp = 78.0

    hlt_setpoint = strike_temp
    hex_setpoint = mashing_temp
    client = factory(
        hlt_setpoint,
        hex_setpoint,
        loop_delay_seconds=.5,
        hangover_delay_seconds=10
    )

    brew_state = client.execute_loop()
    new_time = brew_state.dtime

    delta_time = (new_time-datetime.datetime(1970, 1, 1,tzinfo=pytz.UTC)).total_seconds()
    time.append(delta_time-time_offset)
    temperature.append(brew_state.hlt_temperature)
    flow_rate.append(brew_state.pump_outlet_flowrate)

    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.add_traces({
        'x': list(time),
        'y': list(temperature),
        'name': 'temperature',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.add_traces({
        'x': list(time),
        'y': list(flow_rate),
        'text': list(time),
        'name': 'flow rate',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


""" i think this is actually what we need: 
https://pythonprogramming.net/live-graphs-data-visualization-application-dash-python-tutorial/
"""

