import sys
sys.path.append('/Users/bsl/Desktop/UrbanTraffic')

import pandas as pd

yellow_taxi_2019_03 = pd.read_csv('data/yellow_taxi_2019_03_count.csv')
yellow_taxi_2019_04 = pd.read_csv('data/yellow_taxi_2019_04_count.csv')
yellow_taxi_2019_05 = pd.read_csv('data/yellow_taxi_2019_05_count.csv')
yellow_taxi_2020_03 = pd.read_csv('data/yellow_taxi_2020_03_count.csv')
yellow_taxi_2020_04 = pd.read_csv('data/yellow_taxi_2020_04_count.csv')
yellow_taxi_2020_05 = pd.read_csv('data/yellow_taxi_2020_05_count.csv')

group_data = pd.merge(yellow_taxi_2019_03, yellow_taxi_2019_04, yellow_taxi_2019_05, yellow_taxi_2020_03, yellow_taxi_2020_04, yellow_taxi_2020_05, how='left', left_on=['time'],
right_on=['time'])


from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=True)


nan_data = group_data[group_data['median_home_value'].isna()]
zip_code = list(nan_data['zipcode'].values)
