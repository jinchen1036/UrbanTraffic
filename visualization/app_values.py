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

    def get_attribute_list_dict(self):
        return [{'label': i, 'value': i} for i in self.attributes]

    def set_taxi_heatmap(self, taxi_heatmap):
        self.taxi_heatmap = taxi_heatmap

    def set_taxi_scatter(self, taxi_scatter):
        self.taxi_scatter = taxi_scatter


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

