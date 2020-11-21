import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from data.config import *
from visualization.data_holder import AppData
from visualization.graph_functions import *
from visualization.data_filter import *



Data = AppData()
total_pickup = Data.taxi_trip_filter_df.num_pickup.sum()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(className='app-layout', children=[
    # Time control panel
    html.Div(className="time selection", children=[
        dcc.Loading(
            className="loader",
            id="loading",
            type="default",
            children=[
                dcc.Markdown(id='data_summary_filtered', children='Selected {:,} trips'.format(total_pickup)),
            ]),
    ]),

    html.Div(className="row", id='control-panel-1',style={'width':'100%', 'columnCount': 4},children=[
        html.Div(className="time selection", children=[
            html.Label('Select Year'),
            dcc.RangeSlider(id='year',
                            value=[2019, 2020],
                            min=2019, max=2020,
                            marks={i: str(i) for i in range(2019, 2021)}),
        ]),
        html.Div(className="time selection", children=[
            html.Label('Select Month'),
            dcc.RangeSlider(id='months',
                            value=[3, 5],
                            min=3, max=5,
                            marks={i: str(i) for i in range(3, 6)}),
        ]),

        html.Div(className="time selection", children=[
            html.Label('Select Day'),
            dcc.RangeSlider(id='days',
                            value=[1, 31],
                            min=1, max=31,
                            marks={i: str(i) for i in range(1, 32, 5)}),
        ]),
        html.Div(className="time selection", children=[
            html.Label('Select Hours'),
            dcc.RangeSlider(id='hours',
                            value=[0, 23],
                            min=0, max=23,
                            marks={i: str(i) for i in range(0, 24, 3)}),
        ]),

    ]),
    html.Div(className="row", id='control-panel-2',children=[
        html.Div(className="time selection", children=[
            html.Label('Select a day of week'),
            dcc.Dropdown(id='weekdays',
                         placeholder='Select a day of week',
                         options=[{'label': weekday_name, 'value': index} for index, weekday_name in enumerate(weekday_names)],
                         value=list(range(7)),
                         multi=True),
        ])
    ]),
    html.Div(className="row", children=[
        dcc.Graph(id='geo_map',
                  figure=create_geomap(Data.taxi_trip_filter_df,Data.taxi_geo_json))
    ])
])


# Map figure
@app.callback([Output('geo_map', 'figure'),
               Output('data_summary_filtered', 'children')],
              [Input('year', 'value'),
               Input('months', 'value'),
               Input('days', 'value'),
               Input('hours', 'value'),
               Input('weekdays', 'value')],
              prevent_initial_call=True)
def update_map_figure_by_time(year_range, month_range, days_range, hour_range,weekday_range):
    print(year_range, month_range, days_range, hour_range,weekday_range)
    Data.taxi_trip_filter_df = filter_by_time(Data.taxi_trip_df,Data.taxi_zone_df,
                                              year_range, month_range, days_range, hour_range,weekday_range)
    figure = create_geomap(Data.taxi_trip_filter_df, Data.taxi_geo_json)
    return figure, 'Selected {:,} trips'.format(Data.taxi_trip_filter_df.num_pickup.sum())

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
