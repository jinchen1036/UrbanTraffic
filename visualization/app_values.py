from datetime import date
class AppData:
    def __init__(self, column_names, total_pickup,total_dropoff):
        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.scatter_x = 'avg_trip_distance'
        self.scatter_y = 'avg_total_price'
        self.scale = 'Linear'
        self.attributes = column_names
        self.total_pickup = total_pickup
        self.total_dropoff = total_dropoff

        self.year_range = [2019, 2020]
        self.month_range = [3, 5]
        self.days_range =[1, 31]
        self.hour_range =[0, 23]
        self.weekday_range = list(range(7))

        #
        self.covid_start_date = date(2020, 3, 31)
        self.covid_end_date = date(2020, 5, 17)

    def get_attribute_list_dict(self):
        return [{'label': i, 'value': i} for i in self.attributes]

    def set_taxi_heatmap(self, taxi_heatmap):
        self.taxi_heatmap = taxi_heatmap

    def set_taxi_scatter(self, taxi_scatter):
        self.taxi_scatter = taxi_scatter

    def set_covid_heatmap(self, covid_heatmap):
        self.covid_heatmap = covid_heatmap


    def check_attribute_change(self,value_list):
        '''
        :param value_list: dict of attribute:
            {
                'year_range': [2019, 2020],
                'month_range': [3, 5],
                'days_range': [1, 31],
                'hour_range': [0, 23],
                'weekday_range': [0, 1, 2, 3, 4, 6]
            }
        :return: bool - check if the any value is change
        '''
        change = False
        self_values = vars(self)
        for key, value in value_list.items():
            if self_values[key] != value:
                setattr(self, key, value)
                change = True
        return change


    def check_time_scale_scatter_change(self,year_range, month_range, days_range, hour_range,weekday_range,scale_type, scatter_x,scatter_y):
        # check time  change
        time_dict = {
            'year_range': year_range,
            'month_range': month_range,
            'days_range': days_range,
            'hour_range': hour_range,
            'weekday_range': weekday_range
        }
        time_change = self.check_attribute_change(time_dict)

        # check scale change
        scale_change = self.check_attribute_change({"scale": scale_type})

        # check scatter attribute
        scatter_dict = {
            'scatter_x': scatter_x,
            'scatter_y': scatter_y
        }
        scatter_change = self.check_attribute_change(scatter_dict)

        return time_change, scale_change, scatter_change
