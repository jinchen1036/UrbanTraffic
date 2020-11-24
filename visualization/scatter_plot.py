import plotly.express as px
from visualization.data_holder import AppData



Data = AppData()

# fig = px.scatter(Data.taxi_trip_filter_df, x="avg_total_price", y="avg_trip_speed_mph")
# fig.show()

# if want compare time, need to sum up all data of the same day from the Data.taxi_trip_df

zone_ex = Data.taxi_trip_df[Data.taxi_trip_df['zone']==165] # select by zone

# sample scatter plot： time  vs  num_pickup
fig = px.scatter(Data.taxi_trip_df, x=Data.taxi_trip_df.index, y="num_pickup")
fig.show()
