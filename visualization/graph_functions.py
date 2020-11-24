import numpy as np
import plotly.express as px

def create_geomap(filter_df, geo_json, zoom=10,center={"lat": 40.7, "lon": -73.99}):
    fig = px.choropleth_mapbox(filter_df,
                               geojson=geo_json,
                               # color="num_pickup",
                               color=np.log10(filter_df["num_pickup"]),
                               # showscale = False,
                               locations="zone_name",
                               featureidkey="properties.zone",
                               mapbox_style="carto-positron",
                               hover_data=['num_pickup','num_dropoff','ave_trip_passenger','avg_trip_speed_mph',
                                           'avg_trip_distance', 'avg_total_price','avg_price_per_mile', 'Cash', 'Card',
                                           'zone_name','neighborhood','population','median_household_income','zipcode'],
                               zoom=zoom,
                               center=center,
                               opacity=0.5,
                               color_continuous_scale = px.colors.sequential.Reds,
                               width=1000, height=700
                               )
    
    fig.update_traces(colorbar=None)
    fig.update_traces(showscale=False)
    return fig
