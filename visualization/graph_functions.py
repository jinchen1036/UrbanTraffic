import numpy as np
import plotly.express as px

def create_geomap(filter_df, geo_json, scale, zoom=9.5,center={"lat": 40.7, "lon": -73.99}):

    if scale == "Linear":
        color = filter_df["num_pickup"]
    else:
        color = np.log10(filter_df["num_pickup"])
    fig = px.choropleth_mapbox(filter_df,
                               geojson=geo_json,
                               # color="num_pickup",
                               color=color,
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
                               width=1300, height=600
                               )

    fig.update_traces(colorbar=None)
    fig.update_traces(showscale=False)
    return fig

def create_scatter_plot(filter_df, attribute_x,attribute_y):

    fig = px.scatter(filter_df, x=attribute_x,
                     y=attribute_y, color='borough',
                     hover_name='zone_name')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    # fig.update_xaxes(title=attribute_x)
    # fig.update_yaxes(title=attribute_y)

    return fig
