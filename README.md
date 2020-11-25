# Urban Traffic 

# Dataset 
- [NYC Yellow Taxi Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [NYC Taxi Zones](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)
- [COVID-19 NYC Cases by ZipCode](https://github.com/thecityny/covid-19-nyc-data/blob/master/zcta.csv)
    - Data from **3/31** - **5/17**
- [Zipcode Information](https://pypi.org/project/uszipcode/)

# Setup 
- Clone and install packages and modules
```
    git clone https://github.com/jinchen1036/UrbanTraffic.git
    cd UrbanTraffic
    pip install -r requirements.txt
```
- To update requirements.txt ->  `pip freeze > requirements.txt`

# Visualization
- To run the visualization - have complete the setup 
```
    python app.py
```
- The file for running the visualization is in [**visualization/main.py**](https://github.com/jinchen1036/UrbanTraffic/blob/main/visualization/main.py)
    - [plotly](https://plotly.com/python/plotly-fundamentals/) is use as the main visualization package
    
# Deployment
[Live Link](https://urban-traffic-visualization.herokuapp.com/)
```.env
    git push heroku main 
```

 
# Data Format
### taxi_zone_info_all.csv
- location_id   (taxi zone id)
- zone_name
- borough
- centroid_x    (taxi zone centroid longitude)
- centroid_y    (taxi zone centroid latitude)
- zipcode
- county
- neighborhood
- median_household_income
- median_home_value
- population
- population_density


### covid_info.csv  (`2020/3/31` - `2020/5/17`)
- month
- day
- zipcode
- daily_case
- total_case

### yellow_taxi_all_clean.csv
- Consider the clean yellow taxi data from `2019/03/01` to `2019/05/31` and `2020/03/01` to `2020/05/31`
- Data Fields
    - time
    - zone  (taxi zone id)
    - num_pickup
    - num_dropoff
    - ave_trip_passenger
    - avg_trip_speed_mph
    - avg_trip_distance 
    - avg_total_price
    - avg_price_per_mile
    - Cash (number of cash payment)
    - Card (number of card payment)

