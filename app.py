import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from flask_caching import Cache

from data.config import *
from visualization.data_holder import DataSource
from visualization.app_values import AppData
from visualization.graph_functions import *
from visualization.data_filter import *


Data = DataSource("../data")
AppState = AppData(column_names=Data.taxi_trip_df.columns.values,
                   total_pickup=Data.taxi_trip_filter_df.num_pickup.sum(),
                   total_dropoff = Data.taxi_trip_filter_df.num_dropoff.sum())
AppState.set_taxi_heatmap(create_geomap(Data.taxi_trip_filter_df,Data.taxi_geo_json,AppState.scale))
AppState.set_taxi_scatter(create_scatter_plot(Data.taxi_trip_filter_df, AppState.scatter_x,AppState.scatter_y))
covid_df, zipcode_trip_df = filter_zipcode_by_time(Data.covid_19, Data.zipcode_trip_df, Data.agg_column,
                                                      start_day=AppState.covid_start_date,
                                                      end_day=AppState.covid_end_date)
AppState.set_attribute_names(covid_df, zipcode_trip_df)
AppState.set_covid_heatmap(*create_zipcode_geomap(covid_df,zipcode_trip_df, Data.zipcode_geo_json,
                                                  AppState.covid_attribute_dropdown, AppState.zipcode_trip_attribute_dropdown))
del covid_df, zipcode_trip_df


app = dash.Dash(__name__, external_stylesheets=AppState.external_stylesheets)
server = app.server
app.layout = html.Div(className='app-layout', children=[
    dcc.Tabs(id='main-tab', children=[
        dcc.Tab(label='New York City Traffic', children=[
            # Time control panel
            html.Div(id='display-panel', children=[
                dcc.Loading(
                    className="loader",
                    id="loading",
                    type="default",
                    children=[
                        dcc.Markdown(id='data_summary_filtered', children='## Selected %d trips' % (AppState.total_pickup)),
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
            dcc.Tabs(id='tab', children=[
                dcc.Tab(label='New York City Traffic Geomap', children=[
                    html.Div(style={'width': '20%', 'columnCount': 2}, children=[
                        html.Label('Map Scale: '),
                        dcc.RadioItems(
                            id='scale_type',
                            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value=AppState.scale,
                            labelStyle={'width': '50%', 'display': 'inline-block'}
                        )]
                    ),
                    html.Div(className="row", children=[
                        dcc.Graph(id='geo_map',
                                  figure=AppState.taxi_heatmap)
                    ])
                ]),
                dcc.Tab(label='Compare Traffic Attributes', children=[
                    html.Div(className="row", children=[
                        html.Div([
                            dcc.Dropdown(
                                id='scatter_x',
                                options=AppState.get_attribute_list_dict(AppState.trip_attributes),
                                value=AppState.scatter_x
                            )
                        ],style={'width': '48%', 'display': 'inline-block'}),
                        html.Div([
                            dcc.Dropdown(
                                id='scatter_y',
                                options= AppState.get_attribute_list_dict(AppState.trip_attributes),
                                value=AppState.scatter_y
                            )
                        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
                    ]),
                    html.Div(className="row", children=[
                        dcc.Graph(id='scatter_plot',
                                  figure=AppState.taxi_scatter)
                    ])
                ])
        ])
        ]),
        dcc.Tab(label='Traffic vs COVID-19', children=[
            html.Div([
                html.Div(className="row",children=[
                    html.Div(className="row",children=[
                        html.Label('Picked Data Range'),
                        dcc.DatePickerRange(
                            id='date-picker',
                            min_date_allowed=AppState.covid_start_date,
                            max_date_allowed=AppState.covid_end_date,
                            initial_visible_month=AppState.covid_start_date,
                            start_date=AppState.covid_start_date,
                            end_date=AppState.covid_end_date)
                    ]),
                    html.Div(id='date-picker-warning'),
                ]),
                html.Div(style={'columnCount': 4,'display':'flex'},children=[
                    html.Label('Picked Left Map Attributed'),
                    dcc.Dropdown(
                        id='covid_attribute_dropdown',multi=False,
                        options=AppState.get_attribute_list_dict(AppState.covid_attribute),
                        value=AppState.covid_attribute_dropdown,
                        style={'width': '50%'}
                    ),
                    html.Label('Picked Right Map Attributed'),
                    dcc.Dropdown(
                        id='zipcode_trip_attribute_dropdown',multi=False,
                        options=AppState.get_attribute_list_dict(AppState.zipcode_trip_attribute),
                        value=AppState.zipcode_trip_attribute_dropdown,
                        style={'width': '50%'} #,'padding-left':'10%'
                    )
                ]),
                html.Div(style={'width': '100%', 'columnCount': 2}, children=[
                    html.Div(className="row", children=[dcc.Graph(id='covid-19-map', figure=AppState.covid_heatmap)]),
                    html.Div(className="row",
                             children=[dcc.Graph(id='zipcode-trip-map', figure=AppState.zipcode_trip_heatmap)])
                ]),
                html.Div(id='select-zipcode'),
                html.Div(className="row", style={'width': '100%', 'columnCount': 2}, children=[
                    dcc.Graph(id='select-zipcode-covid-plot', figure={}),
                    dcc.Graph(id='select-zipcode-trip-plot', figure={})
                ])
            ])
        ])
    ])
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
               Input('scale_type', 'value'),
               Input('scatter_x', 'value'),
               Input('scatter_y', 'value')],
              prevent_initial_call=True)
def update_figure_by_time(year_range, month_range, days_range, hour_range,weekday_range,scale_type,scatter_x,scatter_y):
    print(year_range, month_range, days_range, hour_range,weekday_range,scale_type, scatter_x,scatter_y)
    if not weekday_range:
        weekday_range = list(range(7))

    time_change, scale_change, scatter_change = AppState.check_time_scale_scatter_change(year_range, month_range, days_range, hour_range,weekday_range,scale_type, scatter_x,scatter_y)
    if time_change:
        Data.taxi_trip_filter_df = filter_by_time(Data.taxi_trip_df,Data.taxi_zone_df,Data.agg_column,
                                                  year_range, month_range, days_range, hour_range,weekday_range)
        if Data.taxi_trip_filter_df.empty:
            AppState.total_pickup = 0
            return AppState.taxi_heatmap,AppState.taxi_scatter, '## No trip data available for this time period, please reselect the time range'
        AppState.total_pickup = Data.taxi_trip_filter_df.num_pickup.sum()

    if time_change or scale_change:
        geo_figure = create_geomap(Data.taxi_trip_filter_df, Data.taxi_geo_json, AppState.scale)
        AppState.taxi_heatmap = geo_figure
    else:
        geo_figure = AppState.taxi_heatmap

    if time_change or scatter_change:
        scatter_figure = create_scatter_plot(Data.taxi_trip_filter_df, AppState.scatter_x, AppState.scatter_y)
        AppState.taxi_scatter = scatter_figure
    else:
        scatter_figure = AppState.taxi_scatter

    return geo_figure,scatter_figure, '## Selected %d trips' % (AppState.total_pickup)


@app.callback([Output('covid-19-map', 'figure'),
               Output('zipcode-trip-map', 'figure'),
               Output('date-picker-warning','children')],
              [Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date'),
               Input('covid_attribute_dropdown', 'value'),
               Input('zipcode_trip_attribute_dropdown','value')],
              prevent_initial_call=True)
def update_output(start_date, end_date,covid_attribute_dropdown,zipcode_trip_attribute_dropdown):
    # check time  change
    print("Selected Data Range: %s -- %s" % (start_date, end_date))
    print("%s vs %s" % (covid_attribute_dropdown,zipcode_trip_attribute_dropdown))
    if pd.Timestamp(start_date,tz='UTC') not in Data.covid_available_days:
        warning = "There is no data available for %s, please select a different start date" % start_date
        return AppState.covid_heatmap, warning
    elif pd.Timestamp(end_date,tz='UTC') not in Data.covid_available_days:
        warning = "There is no data available for %s, please select a different end date" % end_date
        return AppState.covid_heatmap,AppState.zipcode_trip_heatmap, warning
    else:
        covid_time_dict = {
            'covid_start_date': start_date,  # datetime.fromisoformat(start_date),
            'covid_end_date': end_date,  # datetime.fromisoformat(end_date)
        }
        time_change = AppState.check_attribute_change(covid_time_dict)
        if time_change:
            covid_df, zipcode_trip_df = filter_zipcode_by_time(Data.covid_19, Data.zipcode_trip_df,Data.agg_column,
                                                                  start_day=AppState.covid_start_date,
                                                                  end_day =AppState.covid_end_date)
            AppState.set_attribute_names(covid_df, zipcode_trip_df)

        AppState.covid_attribute_dropdown = covid_attribute_dropdown
        AppState.zipcode_trip_attribute_dropdown = zipcode_trip_attribute_dropdown
        covid_map, zipcode_trip_map = create_zipcode_geomap(AppState.covid_df, AppState.zipcode_trip_df,
                                                            Data.zipcode_geo_json, AppState.covid_attribute_dropdown,
                                                            AppState.zipcode_trip_attribute_dropdown)
        AppState.set_covid_heatmap(covid_map, zipcode_trip_map)
        return covid_map, zipcode_trip_map, ""

@app.callback([Output('select-zipcode-covid-plot','figure'),
               Output('select-zipcode-trip-plot','figure'),
               Output('select-zipcode','children')],
                [Input('covid-19-map', 'clickData'),
                Input('zipcode-trip-map', 'clickData')],
              prevent_initial_call=True)
def click_map(click_covid,click_trip):
    trg = dash.callback_context.triggered
    print('Interaction: click on popular destinations tab detected: %r', trg)

    if click_trip is not None:
        zipcode = click_trip['points'][0]['location']
    else:
        zipcode = click_covid['points'][0]['location'] # 11226 int

    if zipcode in AppState.select_zipcodes:
        AppState.select_zipcodes.remove(zipcode)
    else:
        AppState.select_zipcodes.append(zipcode)

    if not AppState.select_zipcodes:
        return {},{},"### No selected zipcode"
    covid_df, zipcode_trip_df  = get_select_zipcodes_from_time_interval(Data.covid_19, Data.zipcode_trip_df,AppState.select_zipcodes,
                                                                  start_day=AppState.covid_start_date,
                                                                  end_day =AppState.covid_end_date)
    covid_line = create_line_fig_by_zipcode(covid_df, AppState.covid_attribute_dropdown)
    zipcode_trip_line = create_line_fig_by_zipcode(zipcode_trip_df, AppState.zipcode_trip_attribute_dropdown)
    return covid_line, zipcode_trip_line, '### Selected Zipcodes: %s'%(', '.join(map(str, AppState.select_zipcodes)))


if __name__ == '__main__':
    app.run_server(debug=True)
