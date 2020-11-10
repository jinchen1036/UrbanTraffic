import pandas as pd
from uszipcode import SearchEngine
from data_preprocess.zone_distance import get_zone_centroid

taxi_zones = pd.read_csv("data/taxi_zones.csv")
search = SearchEngine(simple_zipcode=True)
zones_info = []

for index, row in taxi_zones.iterrows():
    x, y = get_zone_centroid(row['the_geom'])
    result = search.by_coordinates(y, x)[0]
    zone_info = {
        'location_id': row['LocationID'],
        'zone': row['zone'],
        'borough': row['borough'],
        'centroid_x': x,
        'centroid_y': y,
        'zipcode': result.zipcode,
        'county':result.county,
    }
    zones_info.append(zone_info)

zones_info_df = pd.DataFrame(zones_info)
zones_info_df.to_csv('data/taxi_zone_info.csv',index=False)

