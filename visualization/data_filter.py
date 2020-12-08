import numpy as np
import pandas as pd
# zone 264 and 265 is unknown


def combine_zone_info(data, agg_column, group_by_criteria):
    for name in agg_column:
        data['sum_%s' % name] = data['avg_%s' % name] * data['num_pickup']
        data.drop(columns=['avg_%s' % name], inplace=True)
    group_df = data.groupby(group_by_criteria).agg('sum').reset_index()

    for name in agg_column:
        group_df['avg_%s' % name] = group_df['sum_%s' % name] / group_df['num_pickup']
        group_df.drop(columns=['sum_%s' % name], inplace=True)
    return group_df


def filter_by_time(trip_df, year_range, month_range, days_range, hour_range,weekday_range):
    # start_day = '%04d-%02d-%02d' % (year_range[0],month_range[0], days_range[0])
    # end_day = '%04d-%02d-%02d' % (year_range[1], month_range[1], days_range[1])
    start_time = '%02d:00:00' % hour_range[0]
    end_time = '%02d:00:00'% hour_range[1]

    # select_time = pd.DatetimeIndex([])
    # for year in range(year_range[0], year_range[-1] + 1):
    #     for month in range(month_range[0], month_range[-1] + 1):
    #         if month == 4:
    #             days_range[0] = 30 if days_range[0] == 31 else days_range[0]
    #             days_range[1] = 30 if days_range[1] == 31 else days_range[1]
    #         select_time = select_time.union(pd.date_range(start='%d/%d/%d' % (month, days_range[0], year),
    #                                                       end='%d/%d/%d' % (month, days_range[-1], year)))

    # filter by time
    year  =  np.isin(np.array(trip_df.index.year,dtype=np.int), range(year_range[0], year_range[-1] + 1))
    month = np.isin(np.array(trip_df.index.month, dtype=np.int), range(month_range[0], month_range[-1] + 1))
    day = np.isin(np.array(trip_df.index.day, dtype=np.int), range(days_range[0], days_range[-1] + 1))
    weekday = np.isin(np.array(trip_df.index.weekday,dtype=np.int), weekday_range)

    trip_df = trip_df[year & month & day & weekday]
    return trip_df.between_time(start_time, end_time)


def merge_yellow_taxi_data(df,taxi_zone_df, agg_column):
    # group by zone
    pickup_group_data = combine_zone_info(data=df.reset_index(), agg_column=agg_column,
                                          group_by_criteria='zone')
    merge_df = pd.merge(pickup_group_data, taxi_zone_df, left_on='zone',
                        right_on='zone')  # how='left' remove missing zones
    return merge_df

def filter_zipcode_by_time(covid_df, zipcode_trip, agg_column, start_day, end_day):

    # filter by time
    start_df = covid_df.loc[start_day]
    if end_day == start_day:
        return start_day.rename(columns={"num_test": "num_tests"}, errors="raise")

    end_df = covid_df.loc[end_day, ['zipcode', 'num_cases', 'num_test']]
    final_df = pd.merge(start_df, end_df, how='inner', on=['zipcode'])
    final_df['num_cases'] = final_df['num_cases_y'] - final_df['num_cases_x']
    final_df['num_tests'] = final_df['num_test_y'] - final_df['num_test_x']
    final_df.drop(['num_cases_y', 'num_cases_x','num_test_y','num_test_x'], axis=1, inplace=True)

    # process  zipcode file
    zipcode_trip = zipcode_trip.loc[start_day:end_day]
    zipcode_trip_group = combine_zone_info(data=zipcode_trip.reset_index(), agg_column=agg_column,
                                          group_by_criteria='zipcode')
    return final_df, zipcode_trip_group

def get_select_zipcodes_from_time_interval(covid_df,zipcode_trip, zipcodes ,start_day, end_day):

    # filter by time
    covid_df = covid_df.loc[start_day:end_day]
    zipcode_trip = zipcode_trip.loc[start_day:end_day]

    # filter by zipcodes
    covid_df = covid_df[np.isin(covid_df['zipcode'], zipcodes)]
    zipcode_trip = zipcode_trip[np.isin(zipcode_trip['zipcode'], zipcodes)]

    return covid_df, zipcode_trip

def filter_by_zone_name(filter_df, zone_name):
    in_zone = np.isin(np.array(filter_df.zone, dtype=np.int), zone_name)
    return filter_df[in_zone]
# year_range = [2019, 2020]
# month_range = [3, 4]
# days_range = [17, 30]
# hour_range = [0, 23]
# weekday_range = list(range(7))
#
#
# select_time = pd.DatetimeIndex([])
# for year in range(year_range[0],year_range[-1]+1):
#     for month in range(month_range[0], month_range[-1] + 1):
#         print(year,month)
#         select_time = select_time.union(pd.date_range(start='%d/%d/%d'%(month,days_range[0],year),
#                                              end='%d/%d/%d'%(month,days_range[-1],year)))
#


def filter_barchart_time(trip_df, year_range, month_range, days_range,weekday_range, zone_name):
    hour_range = [0, 23]

    filter_data = filter_by_time(trip_df, year_range, month_range, days_range, hour_range, weekday_range)
    figure_title = "Distribution of All Taxi Zones Data through out 24 Hours"
    if zone_name:
        in_zone = np.isin(np.array(filter_data.zone, dtype=np.int), zone_name)
        filter_data = filter_data[in_zone]
        figure_title = "Distribution of Data through out 24 Hours for Taxi Zones: " + ",".join(map(str, zone_name))

    filter_data = filter_data.groupby([filter_data.index.hour]).mean()
    filter_data = filter_data.reset_index()

    return filter_data, figure_title
