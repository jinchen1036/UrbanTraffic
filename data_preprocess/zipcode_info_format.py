import requests
import pandas as pd
from uszipcode import SearchEngine
from bs4 import BeautifulSoup as BS

search = SearchEngine(simple_zipcode=True)


req = requests.get("https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm")
soup = BS(req.text,'html.parser')
all_rows = [row for row in soup.find_all('table')[0].find_all('tr')]
all_zipcodes = []
for row in all_rows:
    neighborhood = ''
    for zip_info in row.find_all('td'):
        if 'header2' in zip_info.attrs['headers']:
            neighborhood = zip_info.get_text().strip()
        if 'header3' in zip_info.attrs['headers']:
            zip_codes = zip_info.get_text().strip().split(',')
            for zip_code in zip_codes:
                zip_code_info = search.by_zipcode(zip_code.strip())
                all_zipcodes.append({
                    'zipcode': zip_code_info.zipcode,
                    'neighborhood': neighborhood,
                    'county':zip_code_info.county,
                    'median_household_income':zip_code_info.median_household_income,
                    'median_home_value': zip_code_info.median_home_value,
                    'population': zip_code_info.population,
                    'population_density': zip_code_info.population_density
                })

zipcode_info_df = pd.DataFrame(all_zipcodes)
zipcode_info_df.to_csv('data/zipcode_info.csv',index=False)
