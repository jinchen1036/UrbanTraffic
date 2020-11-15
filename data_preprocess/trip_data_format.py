# import vaex
import sys
sys.path.append('/home/jchen/UrbanTraffic')

import pandas as pd
from datetime import timedelta

from data.config import boroughs, weekday_names
from dataAccessor import get_taxi_data,get_zone_info



def format_trip_data(year, month):
    zones_info = get_zone_info()
    trip_data = get_taxi_data(year = year, month = month)


    # Get only need columns
    trip_data = trip_data[['tpep_pickup_datetime','tpep_dropoff_datetime', 'passenger_count','trip_distance','PULocationID', 'DOLocationID','payment_type','total_amount']]

    # trip_data = trip_data.iloc[:10000]

    # show not null count
    trip_data.info(verbose=True, null_counts=True)

    # TO DO: please deal with the row that have nan value
    trip_data.dropna(inplace = True)

    # TO DO: should not include the travel distance to be 0 or less
    trip_data = trip_data[trip_data['trip_distance'] > 0]

    # TO DO: should not include the total price to be 0 or less
    trip_data = trip_data[trip_data['total_amount'] > 0]
    # TO DO:  Please see the `Format_Trip_Data_Note.md` for the payment type detail, decide if should only include Credit card and Cash payment or all
    #         After make the decision, please add a payment_type dict in data/config.py
    # - payment_type
    #     - 1 = Credit card
    #     - 2 = Cash
    #     - 3 = No charge
    #     - 4 = Dispute
    #     - 5 = Unknown
    #     - 6 = Voided trip
    trip_data = trip_data[(trip_data['payment_type']==1) | (trip_data['payment_type']==2)]

    # TO DO: check for other conditions  (e.g., `tpep_dropoff_datetime` should be greater than `tpep_pickup_datetime`)
    different_time = trip_data['tpep_dropoff_datetime'] - trip_data['tpep_pickup_datetime']
    trip_data = trip_data[different_time > timedelta(minutes=1)]
    # can use below line to explore a sample record in the dataset
    row = trip_data.iloc[0]
    def get_trip_duration(trip):
        return (trip['tpep_dropoff_datetime']  - trip['tpep_pickup_datetime']).total_seconds()/60

    trip_data['trip_duration_min'] = trip_data.apply(get_trip_duration, axis=1)
    trip_data['trip_speed_mph'] = trip_data['trip_distance'] /( trip_data['trip_duration_min'] / 60)


    # Extract meaningful info
    format_trips = []
    for index, row in trip_data.iterrows():
        # TO DO: Add other fields that you think should be include (note: all field should be numeric value in order to store in hdf5 file)
        # Can separate time into years and months if you want
        if (row['PULocationID'] in zones_info['location_id'] and row['DOLocationID'] in zones_info['location_id']):
            trip = {
                'pickup_time': row['tpep_pickup_datetime'],
                'pickup_day': weekday_names.index(row['tpep_pickup_datetime'].day_name()),
                'pickup_hour': row['tpep_pickup_datetime'].hour,
                'pickup_zone': row['PULocationID'],
                'pickup_borough':zones_info.loc[zones_info['location_id']==row['PULocationID'], 'borough'].values,

                'dropoff_time': row['tpep_dropoff_datetime'],
                'dropoff_day': weekday_names.index(row['tpep_dropoff_datetime'].day_name()),
                'dropoff_hour': row['tpep_dropoff_datetime'].hour,
                'dropoff_zone': row['DOLocationID'],
                'dropoff_borough': zones_info.loc[zones_info['location_id']==row['DOLocationID'], 'borough'].values,

                'total_price': row['total_amount'],
                'payment_type': row['payment_type'],

                'trip_distance': row['trip_distance'],
                'trip_duration_min': row['trip_duration_min'],
                'trip_speed_mph': row['trip_speed_mph']
            }

            format_trips.append(trip)




    # save process trip data into hdf5 file

    pd.DataFrame(format_trips).to_csv('../data/trip_data/yellow_taxi_%d_%02d.csv'%(year, month),index=False)
    # vaex_df = vaex.from_pandas(pd.DataFrame(format_trips), copy_index=False)
    # vaex_df.export_hdf5('../data/yellow_taxi_%d_%02d.hdf5'%(year, month))


    # read the trip hdf5 file
    # vaex_df_read = vaex.open('data/yellow_taxi_%d_%02d.hdf5'%(year, month))

format_trip_data(year=2020, month=4)
format_trip_data(year=2020, month=5)
format_trip_data(year=2019, month=5)
format_trip_data(year=2019, month=4)
format_trip_data(year=2019, month=3)
