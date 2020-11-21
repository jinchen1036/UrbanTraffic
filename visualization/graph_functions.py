import plotly.express as px

def create_geomap(filter_df, geo_json, zoom=10,center={"lat": 40.7, "lon": -73.99}):
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
                               width=700, height=600
                               )
    return fig
