import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

def create_geomap(filter_df, geo_json, scale, attribute = "num_pickup",zoom=9.5,center={"lat": 40.7, "lon": -73.99}):

    if scale == "Linear":
        color_string = attribute
    else:
        color_string = "LogScale-%s"%attribute
        filter_df[color_string] = np.log10(filter_df[attribute])

    fig = px.choropleth_mapbox(filter_df,
                               geojson=geo_json,
                               # color="num_pickup",
                               color=color_string,
                               # showscale = False,
                               locations="zone_name",
                               featureidkey="properties.zone",
                               mapbox_style="carto-positron",
                               hover_data=['num_pickup','num_dropoff','avg_trip_passenger','avg_trip_speed_mph','avg_trip_distance',
                                           'avg_total_price','avg_price_per_mile', 'num_cash_payment', 'num_card_payment',
                                           'zone_name','neighborhood','population','median_household_income','zipcode','zone'],
                               zoom=zoom,
                               center=center,
                               opacity=0.5,
                               color_continuous_scale = px.colors.sequential.Reds,
                               width=1300, height=670,
                               title=color_string
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



def create_line_fig_by_zipcode(filter_df,attribute_y, color = 'zipcode'):
    fig = px.line(filter_df, x=filter_df.index, y=attribute_y, color=color)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

def create_correlation_heatmap(covid_df, zipcode_trip_df):
    result = pd.merge(covid_df, zipcode_trip_df, left_on='zipcode',right_on='zipcode')
    correlation = result.corr()
    rounds = np.around(correlation.values, decimals=2)
    fig = ff.create_annotated_heatmap(correlation.values, x = list(correlation.columns),
                                      y=list(correlation.columns),
                                      annotation_text = rounds,zmin=-1, zmax=1,
                                      colorscale=px.colors.sequential.RdBu, showscale=True)
    fig.update_layout(
        width=1300, height=700
    )
    return fig

def create_correlation_heatmap_selected_zipcode(covid_df, zipcode_trip_df, zipcode):
    z = zipcode_trip_df[zipcode_trip_df.zipcode == zipcode].resample('D').mean().dropna()
    z.index = z.index.tz_localize(tz='UTC')

    z.reset_index(inplace=True)
    z1 = covid_df[covid_df.zipcode == zipcode].resample('D').mean()
    z1 = z1.reset_index()

    result = pd.merge(z1, z, left_on=['time'],right_on=['time']).dropna()

    if result.empty:
        return {}
    correlation = result[['num_cases', 'num_test', 'num_pickup', 'num_cash_payment', 'num_card_payment', 'num_dropoff',
                          'avg_trip_passenger', 'avg_trip_speed_mph', 'avg_trip_distance',
                          'avg_total_price', 'avg_price_per_mile']].corr()

    rounds = np.around(correlation.values, decimals=2)
    fig = ff.create_annotated_heatmap(correlation.values, x=list(correlation.columns),
                                      y=list(correlation.columns),
                                      annotation_text=rounds, zmin=-1, zmax=1,
                                      colorscale=px.colors.sequential.RdBu, showscale=True)

    # Make text size smaller
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 8

    fig.update_layout(
        width=1200, height=700,title = 'Pearson Correlation of Zipcode %d'%zipcode
    )
    fig['layout']['xaxis']['side'] = 'bottom'

    return fig
