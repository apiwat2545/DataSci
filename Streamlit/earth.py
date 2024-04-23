import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/apiwat2545/RainDaily_Tabular.csv/main/RainDaily_Tabular.csv')

# ข้อมูลสำหรับตัวอย่าง
df = pd.DataFrame(df)

province = st.sidebar.selectbox("Select Province", df["province"].unique())
selected_date = st.sidebar.date_input("Select Date", value=datetime(2017, 8, 1))

selected_date = pd.to_datetime(selected_date)
df["date"] = pd.to_datetime(df["date"])


province_data = df[df["province"] == province]
date_data = df[df["date"].dt.date == selected_date.date()]
date_data = date_data.dropna()
province_avg_rain = date_data.groupby("province")["rain"].mean().sort_values(ascending=False)


st.subheader("สถิติรายวัน")
province_over_time = province_data.groupby("date")["rain"].sum()  # or mean() if you want average
st.bar_chart(province_over_time)


st.subheader("สถิติรายพื้นที่")
if not province_avg_rain.empty:
    st.bar_chart(province_avg_rain)
else:
    st.write("No data available for the selected date.")


st.subheader('แผนที่ปริมาณน้ำฝน')
view = pdk.data_utils.compute_view(df[['longitude', 'latitude']])
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[longitude, latitude]',
    get_radius='rain * 100',
    get_fill_color='[255, 0, 0]',
    pickable=True
)
tooltip = {"html": "<b>{tambon}</b><br />Rain: {rain} mm"}
map_ = pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    map_style='mapbox://styles/mapbox/light-v9',
    tooltip=tooltip
)
st.pydeck_chart(map_)


# Group by province and date, and calculate statistics
province_stats = df.groupby(['province']).agg({'rain': ['max', 'min', 'mean', 'std']})

# Display the calculated statistics
st.write(province_stats)

# Group by date, and calculate statistics
date_stats = df.groupby(['date']).agg({'rain': ['max', 'min', 'mean', 'std']})

# Display the calculated statistics
st.write(date_stats)

# Display code
st.subheader("Code:")
st.code("""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/apiwat2545/RainDaily_Tabular.csv/main/RainDaily_Tabular.csv')

# ข้อมูลสำหรับตัวอย่าง
df = pd.DataFrame(df)

province = st.sidebar.selectbox("Select Province", df["province"].unique())
selected_date = st.sidebar.date_input("Select Date", value=datetime(2017, 8, 1))

selected_date = pd.to_datetime(selected_date)
df["date"] = pd.to_datetime(df["date"])


province_data = df[df["province"] == province]
date_data = df[df["date"].dt.date == selected_date.date()]
date_data = date_data.dropna()
province_avg_rain = date_data.groupby("province")["rain"].mean().sort_values(ascending=False)


st.subheader("สถิติรายวัน")
province_over_time = province_data.groupby("date")["rain"].sum()  # or mean() if you want average
st.bar_chart(province_over_time)


st.subheader("สถิติรายพื้นที่")
if not province_avg_rain.empty:
    st.bar_chart(province_avg_rain)
else:
    st.write("No data available for the selected date.")


st.subheader('แผนที่ปริมาณน้ำฝน')
view = pdk.data_utils.compute_view(df[['longitude', 'latitude']])
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[longitude, latitude]',
    get_radius='rain * 100',
    get_fill_color='[255, 0, 0]',
    pickable=True
)
tooltip = {"html": "<b>{tambon}</b><br />Rain: {rain} mm"}
map_ = pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    map_style='mapbox://styles/mapbox/light-v9',
    tooltip=tooltip
)
st.pydeck_chart(map_)


# Group by province and date, and calculate statistics
province_stats = df.groupby(['province']).agg({'rain': ['max', 'min', 'mean', 'std']})

# Display the calculated statistics
st.write(province_stats)

# Group by date, and calculate statistics
date_stats = df.groupby(['date']).agg({'rain': ['max', 'min', 'mean', 'std']})

# Display the calculated statistics
st.write(date_stats)
        """)



