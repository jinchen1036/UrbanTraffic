# Urban Traffic 

# Dataset 
- [NYC Yellow Taxi Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [NYC Taxi Zones](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)
- [COVID-19 NYC Cases by ZipCode](https://github.com/thecityny/covid-19-nyc-data/blob/master/zcta.csv)
    - Data from **3/31** - **5/17**
### Setup 
- Clone and install packages and modules
```
    git clone https://github.com/jinchen1036/UrbanTraffic.git
    cd UrbanTraffic
    pip install -r requirements.txt
```
- To update requirements.txt    
`pip freeze > requirements.txt`

- See `sample.py` for get yellow taxi raw data
- See `data_preprocess/trip_data_format.py` for format taxi trip data detail
- See `data_preprocess/zipcode_info_format.py` for zip code information 


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
- zipcode
- county

### The zip code info csv file attributes 
- zipcode
- neighborhood  **(can be used to match the region in paper 4)**
- county
- median_household_income
- median_home_value
- population
- population_density

### Trip Hdf5 File
- Hdf5 File is great for store large data (numeric values)
- Vaex is chose to process the data
    - lazy Out-of-Core DataFrames (similar to Pandas) 
    - visualize and explore big datasets
    - To install please type this in terminal: `pip install vaex`
    - [Vaex Documentation](https://vaex.readthedocs.io/en/latest/api.html) 
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
