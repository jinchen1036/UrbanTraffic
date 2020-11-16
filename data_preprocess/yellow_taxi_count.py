import glob
import pandas as pd

yellow_taxi_files = glob.glob('data/yellow_taxi*count.csv')
all_data = []

for filename in yellow_taxi_files:
    all_data.append(pd.read_csv(filename, parse_dates=['time']))

yellow_taxi_group_data = pd.concat(all_data, axis=0, ignore_index=True)


# check for duplication time and zone
clean_data = yellow_taxi_group_data.groupby(['time', 'zone']).sum()
clean_data.reset_index(inplace=True)

clean_data.to_csv('../data/yellow_taxi_all_count.csv',index=False)
