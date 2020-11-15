import sys
sys.path.append('/Users/bsl/Desktop/UrbanTraffic')

import pandas as pd

taxi_zone_data = pd.read_csv('../data/taxi_zone_info.csv')
zipcode_data = pd.read_csv('../data/zipcode_info.csv')

group_data = pd.merge(taxi_zone_data, zipcode_data, how='left', left_on=['zipcode'],
                      right_on=['zipcode'])


def fillNa(attribute):
    d={}
    z = {
        'zipcode': zip_code_info.zipcode,
        'neighborhood': '',
        'county': zip_code_info.county,
        'median_household_income': zip_code_info.median_household_income,
        'median_home_value': zip_code_info.median_home_value,
        'population': zip_code_info.population,
        'population_density': zip_code_info.population_density
    }
    group_data= group_data.fillna(group_data.B.map(z[attribute]))
    return group_data

from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=True)

nan_data = group_data[group_data['median_home_value'].isna()]
zip_code = list(nan_data['zipcode'].values)

# TO DO: For loop to assign nan values
for attribute in nan_data:
    nan_data[nan_data[attribute].isna()][attribute] = nan_data[nan_data[attribute].isna()][attribute].apply(
        fillNa(attribute))


zip_code_info = search.by_zipcode(zip_code[0])
z = {
'zipcode': zip_code_info.zipcode,
'neighborhood': '',
'county': zip_code_info.county,
'median_household_income': zip_code_info.median_household_income,
'median_home_value': zip_code_info.median_home_value,
'population': zip_code_info.population,
'population_density': zip_code_info.population_density
}


group_data.to_csv('../data/taxi-zone-organized.csv', index=False)
