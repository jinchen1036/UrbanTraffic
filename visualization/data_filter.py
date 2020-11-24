import numpy as np
import pandas as pd
# zone 264 and 265 is unknown


def combine_zone_info(data):
    d = {}
    d['num_pickup'] = data['num_pickup'].sum()
    d['num_dropoff'] = data['num_dropoff'].sum()
    d['ave_trip_passenger'] = (data['ave_trip_passenger']*data['num_pickup']).sum()/d['num_pickup']
    d['avg_trip_speed_mph'] = (data['avg_trip_speed_mph']*data['num_pickup']).sum()/d['num_pickup']
    d['avg_trip_distance'] = (data['avg_trip_distance']*data['num_pickup']).sum()/d['num_pickup']
    d['avg_total_price'] = (data['avg_total_price']*data['num_pickup']).sum()/d['num_pickup']
    d['avg_price_per_mile'] = (data['avg_price_per_mile']*data['num_pickup']).sum()/d['num_pickup']
    # d['avg_price_per_mile'] = (data['avg_price_per_mile'] * data['num_pickup']).sum() / d['num_pickup']
    d['Cash'] = data['Cash'].sum()
    d['Card'] = data['Card'].sum()
    return pd.Series(d)#, index=['num_pickup', 'avg_trip_speed_mph', 'avg_trip_distance', 'avg_total_price'])

def combine_zipcode_info(data):
    d = {}
    d['total_case'] = data['daily_case'].sum()

def filter_by_time(trip_df,taxi_zone_df, year_range, month_range, days_range, hour_range,weekday_range):
    if month_range[0] == 4 and days_range[0] == 31:
        days_range[0] = 30
    if month_range[1] == 4 and days_range[1] == 31:
        days_range[1] = 30

    start_day = '%04d-%02d-%02d' % (year_range[0],month_range[0], days_range[0])
    end_day = '%04d-%02d-%02d' % (year_range[1], month_range[1], days_range[1])

    start_time = '%02d:00:00' % hour_range[0]
    end_time = '%02d:00:00'% hour_range[1]

    # filter by time
    df = trip_df.loc[start_day:end_day].between_time(start_time, end_time)
    df = df[np.isin(np.array(df.index.weekday,dtype=np.int), weekday_range)]
    df.reset_index(inplace=True)
    # group by zone
    pickup_group_data = df.groupby('zone').apply(combine_zone_info)
    pickup_group_data.reset_index(inplace=True)
    merge_df = pd.merge(pickup_group_data, taxi_zone_df, left_on='zone',
                        right_on='zone')  # how='left' remove missing zones

    return merge_df


def filter_zipcode_by_time(covid_df,  start_day, end_day):

    # filter by time
    # month_cond = (month_range[0] <= covid_df['month']) & (covid_df['month'] <= month_range[1])
    # day_cond = (days_range[0] <= covid_df['day']) & (covid_df['day'] <= days_range[1])

    start_df = covid_df.loc[start_day]
    end_df = covid_df.loc[end_day, ['zipcode', 'num_cases', 'num_test']]

    final_df = pd.merge(start_df, end_df, how='inner', on=['zipcode'])
    final_df['num_cases'] = final_df['num_cases_y'] - final_df['num_cases_x']
    final_df['num_tests'] = final_df['num_test_y'] - final_df['num_test_x']

    final_df.drop(['num_cases_y', 'num_cases_x','num_test_y','num_test_x'], axis=1, inplace=True)
    return final_df
#
#
# year_range = [2020, 2020]
# month_range = [3, 3]
# days_range = [1, 4]
# hour_range = [0, 23]
# weekday_range = list(range(7))

