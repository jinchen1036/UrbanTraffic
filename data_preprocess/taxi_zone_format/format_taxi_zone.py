import pandas as pd
from uszipcode import SearchEngine
from data_preprocess.taxi_zone_format.zipcode_info import get_zipcode_neighborhood
from data_preprocess.taxi_zone_format.zone_distance import get_zone_centroid

taxi_zones = pd.read_csv("../../data/trip_data/taxi_zones.csv")
zipcode_neighborhood = get_zipcode_neighborhood()

search = SearchEngine(simple_zipcode=True)
zones_info = []

for index, row in taxi_zones.iterrows():
    x, y = get_zone_centroid(row['the_geom'])
    results = search.by_coordinates(y, x)
#33912 #10010
    zip_code_info =  ''
    for result in results:
        if result.state ==  'NY':
            zip_code_info = result
            break
        elif row['borough'] == 'EWR'and result.state == 'NJ':
            zip_code_info = result
            break
    if zip_code_info:
        zone_info = {
            'location_id': row['LocationID'],
            'zone': row['zone'],
            'borough': row['borough'],
            'centroid_x': x,
            'centroid_y': y,
            'zipcode': zip_code_info.zipcode,
            'county':zip_code_info.county,
            'neighborhood': zipcode_neighborhood[zip_code_info.zipcode] if zip_code_info.zipcode in zipcode_neighborhood  else '',
            'median_household_income': zip_code_info.median_household_income,
            'median_home_value': zip_code_info.median_home_value,
            'population': zip_code_info.population,
            'population_density': zip_code_info.population_density
        }
        zones_info.append(zone_info)

zones_info_df = pd.DataFrame(zones_info)

zones_info_df.drop_duplicates(subset ="location_id", inplace = True)
zones_info_df.fillna("",inplace=True)
zones_info_df.to_csv('../../data/taxi_zone_info_all.csv',index=False)
