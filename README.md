# Urban Traffic 

## Dataset 
- [NYC Yellow Taxi Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [NYC Taxi Zones](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)


#### Update requirements.txt    `pip freeze > requirements.txt`


# Data Format

### Format of the taxi zone geo json file
```
{
    'type': 'FeatureCollections', 
    'features': [
        {
            'type':'Feature',
            'geometry':
                {
                    'type': 'MultiPolygon',
                    'coordinates': [
                        [Polygon Points]
                    ]
                },
            'properties':
                {
                    'object_id': row['OBJECTID'],
                    'location_id':row['LocationID'],
                    'zone': row['zone'],
                    'borough': row['borough'],
                    'shape_leng': row['Shape_Leng'],
                    'shape_area': row['Shape_Area']
                }
        },
        ...
    ]
}

```

### The taxi zone info csv file attributes
- location_id
- zone
- borough
- centroid_x
- centroid_y


### Trip Hdf5 File
- Hdf5 File is great for store large data (numeric values)
- Use [vaex](https://vaex.readthedocs.io/en/latest/api.html) 
    - lazy Out-of-Core DataFrames (similar to Pandas) 
    - visualize and explore big tabular datasets
- Data Fields
    - pickup_time
    - pickup_day        (weekday number)
    - pickup_hour
    - pickup_zone
    - pickup_borough    (index of borough - please refer to data/config.py)
    - dropoff_time
    - dropoff_day       (weekday number)
    - dropoff_hour
    - dropoff_zone
    - dropoff_borough   (index of borough - please refer to data/config.py)
    - total_price
    - payment_type
    - trip_distance
    - trip_duration_min
    - trip_speed_mph
