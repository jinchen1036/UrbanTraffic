import pandas as pd

def generate_yellow_url(years, months):
    dates = []
    for year in years:
        for month in months:
            dates.append('https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_%04d-%02d.csv'% (int(year), int(month)))
    return dates

def get_trip_duration(trip):
    return (trip['dropoff_time'] - trip['pickup_time']).total_seconds()/60

def pickup_agg(x):
    d = {}
    d['num_pickup'] = x['passenger_count'].count()
    d['avg_trip_passenger'] = x['passenger_count'].sum()/d['num_pickup']
    d['avg_trip_speed_mph'] = x['trip_speed_mph'].mean()
    d['avg_trip_distance'] = x['trip_distance'].mean()
    d['avg_total_price'] = x['total_price'].mean()

    d['num_cash_payment'] = 0
    d['num_card_payment'] = 0
    payment_type = x['payment_type'].value_counts().to_dict()
    if 2.0 in payment_type:
        d['num_cash_payment'] = payment_type[2.0]
    if 1.0 in payment_type:
        d['num_card_payment'] = payment_type[1.0]
    return pd.Series(d)#, index=['num_pickup', 'avg_trip_speed_mph', 'avg_trip_distance', 'avg_total_price'])

def dropoff_agg(x):
    d = {}
    d['num_dropoff'] = x['passenger_count'].count()
    return pd.Series(d)

def get_borough(zone_id):
    borough = zones_info.loc[zones_info['location_id'] == zone_id, 'borough'].values
    if len(borough) == 1:
        return borough[0]
    else:
        return ""



def format_count(df):
    df['pickup_time'] = df['pickup_time'].dt.to_period('H')
    df['dropoff_time'] = df['dropoff_time'].dt.to_period('H')

    pickup_group_data = df.groupby(['pickup_time','pickup_zone']).apply(pickup_agg)
    dropoff_group_data = df.groupby(['dropoff_time','dropoff_zone']).apply(dropoff_agg)
    pickup_group_data.reset_index(inplace=True)
    dropoff_group_data.reset_index(inplace=True)

    pickup_group_data.rename(columns={"pickup_time": "time", "pickup_zone": "zone"}, inplace=True)
    dropoff_group_data.rename(columns={"dropoff_time": "time", "dropoff_zone": "zone"}, inplace=True)

    group_data = pd.merge(pickup_group_data, dropoff_group_data,  how='left', left_on=['time','zone'], right_on = ['time','zone'])
    group_data.fillna(value=0,inplace=True)
    group_data['num_dropoff']=group_data['num_dropoff'].astype('int64')
    group_data['borough'] = group_data["zone"].apply(get_borough)
    return group_data

print("Start Loading Zone Data")
zones_info = pd.read_csv("../../data/taxi_zone_info_all.csv")
