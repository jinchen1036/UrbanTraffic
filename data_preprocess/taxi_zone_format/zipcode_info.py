import requests
import pandas as pd
from bs4 import BeautifulSoup as BS


def get_zipcode_neighborhood():
    req = requests.get("https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm")
    soup = BS(req.text,'html.parser')
    all_rows = [row for row in soup.find_all('table')[0].find_all('tr')]
    all_zipcodes = {}
    for row in all_rows:
        neighborhood = ''
        for zip_info in row.find_all('td'):
            if 'header2' in zip_info.attrs['headers']:
                neighborhood = zip_info.get_text().strip()
            if 'header3' in zip_info.attrs['headers']:
                zip_codes = zip_info.get_text().strip().split(',')
                for zip_code in zip_codes:
                    all_zipcodes[zip_code.strip()] = neighborhood

    return all_zipcodes
# zipcode_info_df = pd.DataFrame(all_zipcodes)
# zipcode_info_df.to_csv('../data/zipcode_info.csv',index=False)
