import json
import numpy as np
import pandas as pd
from visualization.data_filter import filter_by_time

class AppData:
    def __init__(self):
        self.taxi_geo_json = self.get_taxi_zone_geo()
        self.taxi_zone_df = self.get_taxi_zone()
        self.taxi_trip_df = self.get_yellow_taxi_data()
        self.taxi_trip_filter_df = filter_by_time(self.taxi_trip_df,self.taxi_zone_df, year_range = [2019, 2020],
                                                  month_range = [3, 5], days_range = [1, 31],
                                                  hour_range = [0, 23],weekday_range = list(range(7)))

    def get_taxi_zone_geo(self):
        with open('../data/NYC Taxi Zones.geojson') as f:
            geo_json = json.load(f)
        return geo_json

    def get_taxi_zone(self):
        taxi_zone_info = pd.read_csv('../data/taxi_zone_info_all.csv')
        taxi_zone_info.drop(columns=['centroid_x', 'centroid_y'], inplace=True)
        taxi_zone_info.rename(columns={"location_id": "zone"}, errors="raise", inplace=True)
        return taxi_zone_info

    def get_yellow_taxi_data(self):
        yellow_taxi_data = pd.read_csv('../data/yellow_taxi_all_clean.csv', parse_dates=['time'])
        yellow_taxi_data[['zone', 'num_pickup', 'num_dropoff', 'Cash', 'Card']] = yellow_taxi_data[
            ['zone', 'num_pickup', 'num_dropoff', 'Cash', 'Card']].astype('int32')

        # merge_df = pd.merge(yellow_taxi_data, self.taxi_zone_df, left_on='zone',
        #                     right_on='location_id')  # how='left' remove missing value - zone 264, 265
        # merge_df.drop(columns=['location_id', 'centroid_x', 'centroid_y'], inplace=True)
        # merge_df['weekday_name'] = merge_df['time'].dt.dayofweek

        # remove some error data
        yellow_taxi_data = yellow_taxi_data[yellow_taxi_data['avg_price_per_mile'] < 500]
        # merge_df = merge_df[merge_df['avg_trip_distance'] > 0.1]

        yellow_taxi_data.set_index('time', inplace=True)
        return yellow_taxi_data
