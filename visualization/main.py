import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from visualization.data_retriever import *



def create_geomap(filter_df, zoom=10,center={"lat": 40.7, "lon": -73.99}):
    fig = px.choropleth_mapbox(filter_df,
                               geojson=geo_json,
                               color="num_pickup",
                               locations="zone_name",
                               featureidkey="properties.zone",
                               mapbox_style="carto-positron",
                               hover_data=['zone_name','neighborhood','population','median_household_income','zipcode'],
                               zoom=zoom,
                               center=center,
                               opacity=0.5,
                               )
    return fig


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_original = get_merge_data()
geo_json = get_taxi_zone_geo()


filter_df = df_original.loc['2020-5-12 18:00:00']

figure=create_geomap(filter_df)
figure.show()
