import pandas as pd
import json
# zone 264 and 265 is unknown

def get_taxi_zone_geo():
    with open('../data/NYC Taxi Zones.geojson') as f:
        geo_json = json.load(f)
    return geo_json

def get_merge_data():
    yellow_taxi_data = pd.read_csv('../data/yellow_taxi_all_clean.csv', parse_dates=['time'])
    taxi_zone_info = pd.read_csv('../data/taxi_zone_info_all.csv')

    yellow_taxi_data[['zone', 'num_pickup', 'Cash', 'Card']] = yellow_taxi_data[
        ['zone', 'num_pickup', 'Cash', 'Card']].astype('int32')

    taxi_zone_info.drop(columns=['centroid_x', 'centroid_y', 'borough'], inplace=True)

    merge_df = pd.merge(yellow_taxi_data, taxi_zone_info, left_on='zone',
                 right_on='location_id')  # how='left' remove missing value - zone 264, 265

    merge_df.drop(columns=['location_id'], inplace=True)

    merge_df.set_index('time', inplace=True)
    return merge_df
