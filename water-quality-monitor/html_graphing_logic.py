import pandas as pd
from dash import Dash, html, dcc
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
        dcc.Graph(
            figure=make_figure(time, activewks['Temperature (Sensor 1)'], 
                               "Temperature vs Time", "Temperature"), id='temp-graph'
        ),
        dcc.Graph(
            figure=make_figure(time, activewks['pH (Sensor 2)'], "pH vs Time", "pH"),
            id='ph-graph'
        ),
        dcc.Graph(
            figure=make_figure(time, activewks['Conductivity (Sensor 3)'], "Conductivity vs Time", 
                               "Conductivity"), id='cond-graph'
        ),
        dcc.Graph(
            figure=make_figure(time, activewks['Nitrates (Sensor 4)'], "Nitrates vs Time", 
                               "Nitrates"), id='nitr-graph'
        ),
    ]

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
    *graphs
])

if __name__ == "__main__":
    app.run(debug=True) # Left in debug mode for dev purposes 
    # while True:
    #     datagen.add_data("100", "100", "100", "100")
    #     datagenDelay.sleep(6)