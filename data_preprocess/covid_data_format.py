import pandas as pd

covid_data_url = "https://raw.githubusercontent.com/thecityny/covid-19-nyc-data/master/zcta.csv"
covid_data = pd.read_csv(covid_data_url)
covid_data.dropna(inplace=True)
covid_data['timestamp'] = pd.to_datetime(covid_data['timestamp'])
covid_data['zcta'] = covid_data['zcta'].astype('int32')
format_covid = []
for index, row in covid_data.iterrows():
    covid = {
        'month': row['timestamp'].month,
        'day': row['timestamp'].day,
        'zipcode': row['zcta'],
        'daily_cases': row['positive'],
        'total_cases':  row['total']
    }

    format_covid.append(covid)


covid_data_df = pd.DataFrame(format_covid)
covid_data_df.to_csv('../data/covid_info.csv',index=False)

import vaex
vaex_df = vaex.from_pandas(covid_data_df, copy_index=False)
vaex_df.export_hdf5('../data/covid_info.hdf5')

