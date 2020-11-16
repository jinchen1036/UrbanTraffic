# https://github.com/plotly/datasets
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# edit for your own filepath
url = "https://raw.githubusercontent.com/Ronakete/Data/main/us-states.csv"
df = pd.read_csv(url)
df['location'] = df.apply(lambda row: us_state_abbrev[row.state], axis=1)
df['fatality'] = df.deaths/df.cases
cases_sort_df = df.sort_values(by=['cases', 'deaths'], inplace=False, ascending=False)
death_sort_df = df.sort_values(by=['deaths','cases'], inplace=False, ascending=False)
fatality_sort_df = df.sort_values(by=['fatality'], inplace=False, ascending=False)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Graph(id='map_id'),
    dcc.Graph(id='chart_id')

])

def create_figure_geomap(pickup_counts, zone, zoom=10, center={"lat": 40.7, "lon": -73.99}):
    geomap_data = {
        'count': pickup_counts,
        'log_count': np.log10(pickup_counts),
        'zone_name': list(zmapper.values())
    }

    fig = px.choropleth_mapbox(geomap_data,
                               geojson=geo_json,
                               color="log_count",  # heat color
                               locations="zone_name",
                               featureidkey="properties.zone",
                               mapbox_style="carto-positron",
                               hover_data=['count'],
                               zoom=zoom,
                               center=center,
                               opacity=0.5,
                               )
    # Custom tool-tip
    hovertemplate = '<br>Zone: %{location}' \
                    '<br>Number of trips: %{customdata:.3s}'
    fig.data[0]['hovertemplate'] = hovertemplate
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False, showlegend=False)
    return fig

fig = make_subplots(
    rows=2, cols=4,
    specs=[[{"colspan": 4}, None,None,None],[{}, {}, {}, {}]],
    subplot_titles=("Number of COVID-19 Cases of each US State","Cases", "Deaths", "Fatality Rate","Cases vs Deaths"))
fig.add_trace(go.Choropleth(
    locations=df['location'],  # Spatial coordinates
    z=df['cases'].astype(float),  # Data to be color-coded
    locationmode='USA-states',  # set of locations match entries in `locations`
    colorscale='Reds',
    colorbar_title="Cases",
    name='Number of COVID-19 Cases of each US State ',
    geo='geo',
))
fig.add_trace(go.Bar(x=cases_sort_df["state"], y=cases_sort_df["cases"],name="Number of Cases"),
              row=2, col=1)
fig.add_trace(go.Bar(x=death_sort_df["state"], y=death_sort_df["deaths"],name="Number of Deaths"),
              row=2, col=2)
fig.add_trace(go.Bar(x=fatality_sort_df["state"], y=fatality_sort_df["fatality"],name="Fatality Rate"),
              row=2, col=3)
fig.add_trace(go.Scatter(x=df["cases"], y=df["deaths"],mode='markers',hovertext=df["state"],name="Cases vs Deaths"),
              row=2, col=4)
fig.update_layout(
    geo=dict(scope='usa',domain = dict( x = [0.25,0.75], y = [0.5,1] )),height=1000, width=1800,transition_duration=500)
fig.show()


if __name__ == '__main__':
    app.run_server(debug=True)



