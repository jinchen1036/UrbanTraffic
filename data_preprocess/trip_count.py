import pandas as pd


def pickup_agg(x):
    d = {}
    d['num_pickup'] = x['pickup_hour'].count()
    d['avg_trip_speed_mph'] = x['trip_speed_mph'].mean()
    d['avg_trip_distance'] = x['trip_distance'].mean()
    d['avg_total_price'] = x['total_price'].mean()

    d['Cash'] = 0
    d['Card'] = 0
    payment_type = x['payment_type'].value_counts().to_dict()
    if 2.0 in payment_type:
        d['Cash'] = payment_type[2.0]
    if 1.0 in payment_type:
        d['Card'] = payment_type[1.0]
    return pd.Series(d)#, index=['num_pickup', 'avg_trip_speed_mph', 'avg_trip_distance', 'avg_total_price'])

def dropoff_agg(x):
    d = {}
    d['num_dropoff'] = x['dropoff_hour'].count()
    return pd.Series(d)


def format_trip_count(year,month):
    data = pd.read_csv('../data/trip_data/yellow_taxi_%d_%02d.csv'%(year, month))
    # data['pickup_index'] = data['pickup_time'].apply(lambda x: x[5:13])
    data['pickup_time'] = pd.to_datetime(data['pickup_time']).dt.to_period('H')
    data['dropoff_time'] = pd.to_datetime(data['dropoff_time']).dt.to_period('H')


    pickup_group_data = data.groupby(['pickup_time','pickup_zone']).apply(pickup_agg)
    dropoff_group_data = data.groupby(['dropoff_time','dropoff_zone']).apply(dropoff_agg)
    pickup_group_data.reset_index(inplace=True)
    dropoff_group_data.reset_index(inplace=True)


    pickup_group_data.rename(columns={"pickup_time": "time", "pickup_zone": "zone"}, inplace=True)
    dropoff_group_data.rename(columns={"dropoff_time": "time", "dropoff_zone": "zone"}, inplace=True)

    group_data = pd.merge(pickup_group_data, dropoff_group_data,  how='left', left_on=['time','zone'], right_on = ['time','zone'])
    group_data.fillna(value=0,inplace=True)
    group_data['num_dropoff']=group_data['num_dropoff'].astype('int64')
    group_data.to_csv('../data/yellow_taxi_%d_%02d_count.csv' % (year, month), index=False)


format_trip_count(year=2020, month=3)
format_trip_count(year=2020, month=4)
format_trip_count(year=2020, month=5)
format_trip_count(year=2019, month=5)
format_trip_count(year=2019, month=4)
format_trip_count(year=2019, month=3)



