import json
import pandas as pd

taxi_zones = pd.read_csv("data/taxi_zones.csv")

taxi_zone_geo_json = {'type': 'FeatureCollections', 'features': []}
for index, row in taxi_zones.iterrows():
    zone_geo = row['the_geom']
    zone_geo = zone_geo[zone_geo.index('('):].strip().split('(')
    coordinates =  []
    for index, poly in enumerate(zone_geo):
        if poly:
            points = poly.strip().split(',')
            float_points = []
            for p in points:
                if p:
                    x, y = p.strip().split(' ')
                    if ')' in y:
                        y = y[:y.index(')')]
                    float_points.append([float(x), float(y)])
            coordinates.append([float_points])
    zone_json = {'type':'Feature',
                 'geometry':{
                    'type': 'MultiPolygon',
                    'coordinates': coordinates},
                 'properties':{
                    'object_id': row['OBJECTID'],
                    'location_id':row['LocationID'],
                    'zone': row['zone'],
                    'borough': row['borough'],
                    'shape_leng': row['Shape_Leng'],
                    'shape_area': row['Shape_Area']
                }}
    taxi_zone_geo_json['features'].append(zone_json)

with open('data/taxi_zone_geo.json', 'w') as fp:
    json.dump(taxi_zone_geo_json, fp)
