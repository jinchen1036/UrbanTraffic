import glob
import pandas as pd

yellow_taxi_files = glob.glob('../../data/trip_data/yellow_taxi_all_count_by_dask*.csv')
zone_data = pd.read_csv('../../data/taxi_zone_info_all.csv')
all_data = []

for filename in yellow_taxi_files:
    all_data.append(pd.read_csv(filename, parse_dates=['time']))

yellow_taxi_group_data = pd.concat(all_data, axis=0, ignore_index=True)


# check for duplication time and zone
yellow_taxi_group_data = yellow_taxi_group_data.groupby(['time', 'zone']).sum()
yellow_taxi_group_data.reset_index(inplace=True)

# remove unneed time
yellow_taxi_group_data.set_index('time', inplace=True)
data_2019 = yellow_taxi_group_data.loc['2019-03-01 00:00:00':'2019-05-31 23:59:59']
data_2020 = yellow_taxi_group_data.loc['2020-03-01 00:00:00':'2020-05-31 23:59:59']

clean_data = pd.concat([data_2019,data_2020], axis=0, ignore_index=False)
clean_data['avg_price_per_mile'] = clean_data['avg_total_price']/clean_data['avg_trip_distance']
clean_data.reset_index(inplace=True)

