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
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from visualization.data_filter import *


#Initialize figure with subplots
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("2019 - Total Number of Pick-ups by Month", "2020 - Total Number of Pick-ups by Month"),
                    x_title='Month',
                    y_title = 'Total Number of Pick-ups',
                    shared_yaxes= True
                    )

#Fetch data
Data = AppData().taxi_trip_df

#create filter condition based on year
condition_2019 = Data.index.year == 2019
condition_2020 = Data.index.year == 2020

#create separate dataframe
df_2019 =  Data[condition_2019].groupby(by = Data[condition_2019].index.month,as_index= True).agg("sum")
df_2020=  Data[condition_2020].groupby(by = Data[condition_2020].index.month,as_index= True).agg("sum")

#Add graphs
fig.add_trace(go.Bar(x=df_2019.index, y= df_2019["num_pickup"], name = "Year = 2019", text = df_2019["num_pickup"]), row = 1, col=1)
fig.add_trace(go.Bar(x=df_2020.index, y= df_2020["num_pickup"],name = "Year = 2020", text = df_2020["num_pickup"]), row = 1, col=2)


#update the layout and styles to x and y axis and ticks
fig.update_traces(texttemplate='%{text:.4s}', textposition='outside', width = [0.8,0.8,0.8],
                  marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.6)

fig.update_layout(font_family = 'Rockwell',
                  xaxis1 = dict(tickvals = [3,4,5], ticktext = ['March', 'April', 'May']),
                  xaxis2 = dict(tickvals = [3,4,5], ticktext = ['March', 'April', 'May']))

fig.update_xaxes(title_font=dict(size=18,family='Rockwell', color='rgb(8,48,107)'),
                 tickfont=dict(family='Rockwell', color='rgb(8,48,107)', size=12)
                 )
fig.update_yaxes(title_font=dict(size=18,family='Rockwell', color='rgb(8,48,107)'),
                 tickfont=dict(family='Rockwell', color='rgb(8,48,107)', size=12)
                 )

#render the graph
fig.show()