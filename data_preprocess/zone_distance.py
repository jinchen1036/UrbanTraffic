def get_polygon_centroid(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    centroid = (sum(x) / len(points), sum(y) / len(points))
    return centroid

def get_points(multipolygon_string):
    zone_geo = multipolygon_string[multipolygon_string.index('('):].strip().split('(')
    coordinates = []
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
            coordinates.append(float_points)
    return coordinates

def get_zone_centroid(multipolygon_string):
    polygons = get_points(multipolygon_string)
    polygons_centroid = []
    for polygon in polygons:
        polygons_centroid.append(get_polygon_centroid(polygon))

    return get_polygon_centroid(polygons_centroid)
