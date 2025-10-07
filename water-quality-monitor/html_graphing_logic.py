import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as graphobj

# Included modules to repeatedly generate "new" data
import datagen as datagen
import time as datagenDelay

app = Dash(__name__)

try:
    activewks = pd.read_excel("water_quality_data.xlsx")
except FileNotFoundError:
    activewks = pd.DataFrame({'Error': ['Excel sheet not found!']})
except Exception as e:
    activewks = pd.DataFrame({'Error': ['An error has occurred.']})

def make_figure(x, y, title, yaxis_label):
    return graphobj.Figure(
        data=[graphobj.Scatter(x=x, y=y, mode='lines')],
        layout=graphobj.Layout(title=title, xaxis_title='Time (dd/mm/yy hh:mm:ss)', 
                         yaxis_title=yaxis_label)
    )

graphs = []
if 'Error' not in activewks.columns and not activewks.empty:
    time = activewks['Timestamp']
    graphs = [
        dcc.Graph(id='temp-graph'),
        dcc.Graph(id='ph-graph'),
        dcc.Graph(id='cond-graph'),
        dcc.Graph(id='nitr-graph'),
    ]
    
@app.callback(
    [
        Output('temp-graph', 'figure'),
        Output('ph-graph', 'figure'),
        Output('cond-graph', 'figure'),
        Output('nitr-graph', 'figure'),      
    ],
    Input('refresh_interval', 'n_intervals')
)

def update_graphs(n_intervals):
        datagen.add_random_data()
        datagenDelay.sleep(0.5)
        
        updated_data = pd.read_excel("water_quality_data.xlsx")
        
        updated_time = updated_data['Timestamp']
        update_temp = make_figure(updated_time, updated_data['Temperature (Sensor 1)'], 
                               "Temperature vs Time", "Temperature")
        update_ph = make_figure(updated_time, updated_data['pH (Sensor 2)'], 
                               "pH vs Time", "pH")
        update_cond = make_figure(updated_time, updated_data['Conductivity (Sensor 3)'], 
                               "Conductivity vs Time", "Conductivity")
        update_nitr = make_figure(updated_time, updated_data['Nitrates (Sensor 4)'], 
                               "Nitrates vs Time", "Nitrates")
        return update_temp, update_ph, update_cond, update_nitr


app.layout = html.Div([
    html.H1(
        "Water Quality Data Plots", 
        style={
            'textAlign': 'center',
            'font-family': 'Open Sans, verdana, Helvetica, arial, sans-serif',
            'font-weight': '400'
            }), 
    html.H4(
        "These are the collated data plots for our various sensors aboard Abzu.", 
        style={
            'textAlign': 'center',
            'font-family': 'Open Sans, verdana, Helvetica, arial, sans-serif',
            'font-weight': '400'
            }),
    html.Div([
        html.Img(
            src= "https://i.postimg.cc/V6jpqGQK/image.png", 
            alt= "The Abzu logo.", 
            style={
                'width': '50%', 
                'max-width': '500px', 
                'height': 'auto'
                }
            )], 
        style= {'textAlign': 'center'}),
    dcc.Interval(
        id='refresh_interval',
        interval=10*1000,
        n_intervals=0
    ),
    *graphs
])

if __name__ == "__main__":
    app.run(debug=True) 