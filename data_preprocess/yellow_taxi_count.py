import sys
sys.path.append('/Users/bsl/Desktop/UrbanTraffic')

import pandas as pd

yellow_taxi_2019_03 = pd.read_csv('data/yellow_taxi_2019_03_count.csv')
yellow_taxi_2019_04 = pd.read_csv('data/yellow_taxi_2019_04_count.csv')
yellow_taxi_2019_05 = pd.read_csv('data/yellow_taxi_2019_05_count.csv')
yellow_taxi_2020_03 = pd.read_csv('data/yellow_taxi_2020_03_count.csv')
yellow_taxi_2020_04 = pd.read_csv('data/yellow_taxi_2020_04_count.csv')
yellow_taxi_2020_05 = pd.read_csv('data/yellow_taxi_2020_05_count.csv')

yellow_taxi_group_data = pd.concat([yellow_taxi_2019_03,yellow_taxi_2019_04, yellow_taxi_2019_05,
                        yellow_taxi_2020_03, yellow_taxi_2020_04, yellow_taxi_2020_05])


from uszipcode import SearchEngine


