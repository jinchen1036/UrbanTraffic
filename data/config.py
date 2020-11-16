boroughs = ["Bronx", "Brooklyn", "EWR", "Manhattan","Queens", "Staten Island"]
weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

keep_col = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance', 'PULocationID',
         'DOLocationID', 'payment_type', 'total_amount']
drop_col = ['VendorID','RatecodeID','store_and_fwd_flag','fare_amount','extra','mta_tax','tip_amount','tolls_amount','improvement_surcharge','congestion_surcharge']
