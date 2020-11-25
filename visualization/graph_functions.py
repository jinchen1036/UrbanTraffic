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
                               hover_data=['num_pickup','num_dropoff','avg_trip_passenger','avg_trip_speed_mph','avg_trip_distance',
                                           'avg_total_price','avg_price_per_mile', 'num_cash_payment', 'num_card_payment',
                                           'zone_name','neighborhood','population','median_household_income','zipcode'],
                               zoom=zoom,
                               center=center,
                               opacity=0.5,
                               color_continuous_scale = px.colors.sequential.Reds,
                               width=1300, height=600
                               )


    # fig.update_traces(coloraxis_showscale=False, showlegend=False)
    return fig

def create_scatter_plot(filter_df, attribute_x,attribute_y):

    fig = px.scatter(filter_df, x=attribute_x,
                     y=attribute_y, color='borough',
                     hover_name='zone_name')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    # fig.update_xaxes(title=attribute_x)
    # fig.update_yaxes(title=attribute_y)

    return fig

def create_zipcode_geomap(covid_df, zipcode_trip_df, geo_json, covid_attr,zipcode_attr, zoom=9,center={"lat": 40.7, "lon": -73.99}):
    covid_fig = px.choropleth_mapbox(covid_df,
                                     geojson=geo_json,
                                     color=covid_attr,
                                     locations="zipcode",
                                     featureidkey="properties.postalCode",
                                     mapbox_style="carto-positron",
                                     hover_data=['neighborhood','population','median_household_income','zipcode','num_tests'],
                                     zoom=zoom,center=center,opacity=0.5,
                                     color_continuous_scale = px.colors.sequential.Reds,
                                     title="COVID-19 Data",
                                     width=730, height=600
                                     )
    zipcode_trip_fig = px.choropleth_mapbox(zipcode_trip_df,
                               geojson=geo_json,
                               color=zipcode_attr,
                               locations="zipcode",
                               featureidkey="properties.postalCode",
                               mapbox_style="carto-positron",
                               hover_data=['num_cash_payment', 'num_card_payment','num_dropoff', 'avg_trip_passenger',
                                           'avg_trip_speed_mph','avg_trip_distance', 'avg_total_price',
                                           'avg_price_per_mile'],
                               zoom=zoom,center=center,opacity=0.5,
                               color_continuous_scale = px.colors.sequential.Reds,
                               title="NYC Yellow Taxi Data",
                               width=730, height=600
                               )
    return covid_fig, zipcode_trip_fig



def create_line_fig_by_zipcode(filter_df,attribute_y):
    fig = px.line(filter_df, x=filter_df.index, y=attribute_y, color='zipcode')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig
