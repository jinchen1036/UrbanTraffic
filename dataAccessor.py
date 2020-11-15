# https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-03.csv
#  https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2019-01.csv

import pandas as pd

def get_taxi_data(year, month):
    url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_%04d-%02d.csv' % (int(year), int(month))
    data = pd.read_csv(url)
    data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
    data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])
    return data

def get_zone_info():
    return pd.read_csv("../data/taxi_zone_info.csv")
