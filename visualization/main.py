import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from data.config import *
from visualization.data_holder import DataSource
from visualization.app_values import AppData
from visualization.graph_functions import *
from visualization.data_filter import *



Data = DataSource()
AppState = AppData(column_names=Data.taxi_trip_df.columns.values,
                   total_pickup=Data.taxi_trip_filter_df.num_pickup.sum(),
                   total_dropoff = Data.taxi_trip_filter_df.num_dropoff.sum())

app = dash.Dash(__name__, external_stylesheets=AppState.external_stylesheets)
app.layout = html.Div(className='app-layout', children=[
    # Time control panel
    html.Div(className="time selection", children=[
        dcc.Loading(
            className="loader",
            id="loading",
            type="default",
            children=[
                dcc.Markdown(id='data_summary_filtered', children='Selected {:,} trips'.format(AppState.total_pickup)),
            ]),
    ]),

    html.Div(className="row", id='control-panel-1',style={'width':'100%', 'columnCount': 4},children=[
        html.Div(className="time selection", children=[
            html.Label('Select Year'),
            dcc.RangeSlider(id='year',
                            value=AppState.year_range,
                            min=AppState.year_range[0], max=AppState.year_range[-1],
                            marks={i: str(i) for i in AppState.year_range}),
        ]),
        html.Div(className="time selection", children=[
            html.Label('Select Month'),
            dcc.RangeSlider(id='months',
                            value=AppState.month_range,
                            min=AppState.month_range[0], max=AppState.month_range[-1],
                            marks={i: str(i) for i in range(AppState.month_range[0], AppState.month_range[-1]+1)}),
        ]),
        html.Div(className="time selection", children=[
            html.Label('Select Day'),
            dcc.RangeSlider(id='days',
                            value=AppState.days_range,
                            min=AppState.days_range[0], max=AppState.days_range[-1],
                            marks={i: str(i) for i in range(AppState.days_range[0], AppState.days_range[-1]+1, 5)}),
        ]),
        html.Div(className="time selection", children=[
            html.Label('Select Hours'),
            dcc.RangeSlider(id='hours',
                            value=AppState.hour_range,
                            min=AppState.hour_range[0], max=AppState.hour_range[-1],
                            marks={i: str(i) for i in range(AppState.hour_range[0], AppState.hour_range[-1]+1, 3)}),
        ]),
    ]),
    html.Div(className="row", id='control-panel-2',children=[
        html.Div(className="time selection", children=[
            html.Label('Select a day of week'),
            dcc.Dropdown(id='weekdays',
                         placeholder='Select a day of week',
                         options=[{'label': weekday_name, 'value': index} for index, weekday_name in enumerate(weekday_names)],
                         value=AppState.weekday_range,
                         multi=True),
        ])
    ]),
    html.Div(className="row", children=[
        dcc.Graph(id='geo_map',
                  figure=create_geomap(Data.taxi_trip_filter_df,Data.taxi_geo_json))
    ]),
    html.Div(className="row", children=[
        html.Div([
            dcc.Dropdown(
                id='scatter_x',
                options=AppState.get_attribute_list_dict(),
                value=AppState.scatter_x
            )
        ],style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='scatter_y',
                options= AppState.get_attribute_list_dict(),
                value=AppState.scatter_y
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    html.Div(className="row", children=[
        dcc.Graph(id='scatter_plot',
                  figure=create_scatter_plot(Data.taxi_trip_filter_df, AppState.scatter_x,AppState.scatter_y))
    ]),
])


# Update figures by select time
@app.callback([Output('geo_map', 'figure'),
               Output('scatter_plot', 'figure'),
               Output('data_summary_filtered', 'children')],
              [Input('year', 'value'),
               Input('months', 'value'),
               Input('days', 'value'),
               Input('hours', 'value'),
               Input('weekdays', 'value'),
               Input('scatter_x', 'value'),
               Input('scatter_y', 'value'),
               Input('geo_map', 'figure'),],
              prevent_initial_call=True)
def update_figure_by_time(year_range, month_range, days_range, hour_range,weekday_range,scatter_x,scatter_y, geo_figure):
    print(year_range, month_range, days_range, hour_range,weekday_range,scatter_x,scatter_y)

    # check time  change
    time_dict = {
        'year_range': year_range,
        'month_range': month_range,
        'days_range': days_range,
        'hour_range': hour_range,
        'weekday_range': weekday_range
    }
    time_change = AppState.check_attribute_change(time_dict)
    if time_change:
        Data.taxi_trip_filter_df = filter_by_time(Data.taxi_trip_df,Data.taxi_zone_df,
                                                  year_range, month_range, days_range, hour_range,weekday_range)
        geo_figure = create_geomap(Data.taxi_trip_filter_df, Data.taxi_geo_json)
    # check scatter attribute
    scatter_dict = {
        'scatter_x':scatter_x,
        'scatter_y':scatter_y
    }
    scatter_change = AppState.check_attribute_change(scatter_dict)
    scatter_figure = create_scatter_plot(Data.taxi_trip_filter_df, AppState.scatter_x, AppState.scatter_y)
    return geo_figure,scatter_figure, 'Selected {:,} trips'.format(Data.taxi_trip_filter_df.num_pickup.sum())


# # Update scatter by change attribute
# # Update figures by select time
# @app.callback(Output('scatter_plot', 'figure'),
#               [Input('scatter_x', 'value'),
#                Input('scatter_y', 'value')],
#               prevent_initial_call=True)
# def update_scatter_plot(scatter_x, scatter_y):
#     AppState.scatter_x = scatter_x
#     AppState.scatter_y = scatter_y
#     scatter_figure = create_scatter_plot(Data.taxi_trip_filter_df, AppState.scatter_x,AppState.scatter_y)
#     return scatter_figure

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
