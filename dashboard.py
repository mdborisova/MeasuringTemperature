import dash
import numpy as np
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from flask import Flask, request
from flask_restful import Resource, Api

server = Flask('my_app')
app = dash.Dash(server=server)
api = Api(server)

t_history = (np.random.rand(10) * 2 + 16).tolist()

class Temperature(Resource):
    def put(self):
        t_history.append(request.form['t'])


api.add_resource(Temperature, '/api')

app.layout = html.Div([
    dcc.Interval(id='my_interval', disabled=False, n_intervals=0, interval=1000),
    
    html.H1(children='Maria Savinova Dashboard'),

    html.H1(children='Temperature'),

    html.Div(
        children=[
            dcc.Graph(id='temperature')
        ],
        style={'textAlign': 'center'}
    )
])

@app.callback(
    Output('temperature', 'figure'),
    Input('my_interval', 'n_intervals')
)
def update_figure(v):
    return px.line(y=t_history, labels={'x': 'index', 'y': 't'})

if __name__ == '__main__':
    app.run_server(debug=True)
