import io
import requests
import pandas as pd
from uszipcode import SearchEngine
from data_preprocess.taxi_zone_format.zipcode_info import get_zipcode_neighborhood
search = SearchEngine(simple_zipcode=True)
zipcode_neighborhood = get_zipcode_neighborhood()


covid_data_url = "https://raw.githubusercontent.com/thecityny/covid-19-nyc-data/master/zcta.csv"
temp_data = requests.get(covid_data_url).content
covid_data=pd.read_csv(io.StringIO(temp_data.decode('utf-8')))
covid_data.dropna(inplace=True)

covid_data['timestamp'] = pd.to_datetime(covid_data['timestamp'])
covid_data['zcta'] = covid_data['zcta'].astype('int32')
format_covid = []
for index, row in covid_data.iterrows():
    zip_code_info = search.by_zipcode(row['zcta'])
    covid = {
        'time': row['timestamp'],
        'zipcode': row['zcta'],
        'num_cases': row['positive'],
        'num_test':  row['total'],
        'county': zip_code_info.county,
        'neighborhood': zipcode_neighborhood[
            zip_code_info.zipcode] if zip_code_info.zipcode in zipcode_neighborhood else 'unknow',
        'median_household_income': zip_code_info.median_household_income,
        'median_home_value': zip_code_info.median_home_value,
        'population': zip_code_info.population,
        'population_density': zip_code_info.population_density
    }

    format_covid.append(covid)


covid_data_df = pd.DataFrame(format_covid)
covid_data_df.dropna(inplace=True)
covid_data_df.to_csv('../data/covid_info.csv',index=False)
#
# import vaex
# vaex_df = vaex.from_pandas(covid_data_df, copy_index=False)
# vaex_df.export_hdf5('../data/covid_info.hdf5')

