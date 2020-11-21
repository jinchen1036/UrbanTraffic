# import pandas as pd
# import dask.bag as db
# from datetime import timedelta
# import dask.dataframe as dd
# import aiohttp
# import requests
import pandas as pd
from data.config import drop_col
from  data_preprocess.yellow_taxi_format.trip_format_helper import *

# dates = generate_data_seq(years=[2019,2020], months=[3,4,5])
# data = db.from_sequence(dates).map(load).map(clean_trip).filter(filter_trip).map(agg_new_field).map(format_count)
# result = data.compute()



def process_data(urls,name):
    # data = dd.read_csv(urls,parse_dates = ['tpep_pickup_datetime','tpep_dropoff_datetime'],assume_missing=True)
    # data = data.repartition(partition_size="100MB")
    # print("number of partition =  %d"%data.npartitions)

    data = pd.read_csv(urls,parse_dates = ['tpep_pickup_datetime','tpep_dropoff_datetime'])

    #  clean data
    print("Start Clean Data")
    data = data.drop(drop_col, axis=1)
    data = data.dropna()
    data = data.rename(columns={"tpep_pickup_datetime": "pickup_time",
                       "PULocationID": "pickup_zone",
                       "tpep_dropoff_datetime": "dropoff_time",
                       "DOLocationID": "dropoff_zone",
                       "total_amount": "total_price"})

    # agg
    data['trip_duration_min'] = data.apply(get_trip_duration, axis=1)

    # filter data
    print("Start Filter Data")
    c1 = (data['trip_distance'] > 0) & (data['total_price'] > 0)
    c2 = (data['payment_type'] == 1) | (data['payment_type'] == 2)
    c3 = (data['trip_duration_min']>1)

    filter_data =data.loc[c1&c2&c3]
    filter_data['trip_speed_mph'] = filter_data['trip_distance'] / (filter_data['trip_duration_min'] / 60)

    #  compute count
    print("Start Group Data")
    filter_data['pickup_time'] = filter_data['pickup_time'].dt.to_period('H')
    filter_data['dropoff_time'] = filter_data['dropoff_time'].dt.to_period('H')

    pickup_group_data = filter_data.groupby(['pickup_time', 'pickup_zone']).apply(pickup_agg)
    dropoff_group_data = filter_data.groupby(['dropoff_time', 'dropoff_zone']).apply(dropoff_agg)
    pickup_group_data = pickup_group_data.reset_index()
    dropoff_group_data = dropoff_group_data.reset_index()

    pickup_group_data = pickup_group_data.rename(columns={"pickup_time": "time", "pickup_zone": "zone"})
    dropoff_group_data = dropoff_group_data.rename(columns={"dropoff_time": "time", "dropoff_zone": "zone"})

    # group_data = dd.merge(pickup_group_data, dropoff_group_data, on=['time', 'zone'])
    group_data = pd.merge(pickup_group_data, dropoff_group_data, how='left', left_on=['time', 'zone'],
                          right_on=['time', 'zone'])
    group_data = group_data.fillna(value=0)
    group_data['num_dropoff'] = group_data['num_dropoff'].astype('int64')
    group_data['borough'] = group_data["zone"].apply(get_borough)


    # group = format_count(filter_data)
    # compute count

    # z = group_data.compute()
    print("Start Save Computed Trip Data")
    group_data.to_csv('../../data/yellow_taxi_all_count_by_dask_%s.csv'%name,index=False)



# print("Setup 2020 Trip Data")
# process_data(urls = generate_yellow_url(years=[2020], months=[3,4,5]),name = "2020")




# process due large file cause the runtime error

print("Setup 2019 Trip Data")
process_data(urls = generate_yellow_url(years=[2019], months=[3])[0],name = "2019_3")

print("Setup 2019 Trip Data")
process_data(urls = generate_yellow_url(years=[2019], months=[4])[0],name = "2019_4")

print("Setup 2019 Trip Data")
process_data(urls = generate_yellow_url(years=[2019], months=[5])[0],name = "2019_5")
