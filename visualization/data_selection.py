from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
from visualization.data_holder import DataSource
from visualization.data_filter import filter_zipcode_by_time
from visualization.graph_functions import create_zipcode_geomap
Data = DataSource()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2020, 3, 31),
        max_date_allowed=date(2020, 5, 17),
        initial_visible_month=date(2020, 3, 31),
        start_date=date(2020, 3, 31),
        end_date=date(2020, 5, 17)
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Div(className="row", children=[dcc.Graph(id='plot') ])
])


@app.callback(
    [dash.dependencies.Output('output-container-date-picker-range', 'children'),
     dash.dependencies.Output('plot', 'figure')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix += 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix += 'End Date: ' + end_date_string


    print(start_date_string,end_date_string)
    df = filter_zipcode_by_time(Data.covid_19, start_date_string, end_date_string)
    fig = create_zipcode_geomap(df, Data.zipcode_geo_json)

    return string_prefix, fig




if __name__ == '__main__':
    app.run_server(debug=True)
