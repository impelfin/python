import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

from pandas_datareader import data as web 
from datetime import datetime as dt

app = dash.Dash('Hello World',
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],  
        value='COKE'
    ),  
    dcc.Graph(id='my-graph')
], style={'width': '500'})

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = web.DataReader(
        selected_dropdown_value,
        'yahoo',
        dt(2017, 1, 1), 
        dt.now()
    )   
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }], 
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }   

if __name__ == '__main__':
    app.run_server()