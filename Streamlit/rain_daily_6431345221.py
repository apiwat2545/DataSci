import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import pydeck as pdk

df = pd.read_csv('RainDaily_Tabular.csv')

# Sidebar
st.sidebar.header('Sidebar Controls')
option = st.sidebar.selectbox(
    'Visual Options',
    ('Province', 'Date')
)
st.sidebar.write('You selected:', option)

# Main content
st.title('Daily raining visualization')

# Using container
with st.container():
    st.header('Interactive Data Visualization')
    st.write('The chart in Column 1 based on sidebar selections.')

#first part
st.write('\n')
st.header('Column 1: visualization')
if True:
    if option == 'Province':
        average_rain_by_province = df.groupby('province')['rain'].mean().sort_values().reset_index()
        fig = px.bar(average_rain_by_province, x='province', y='rain', 
             labels={'province':'Province', 'rain':'Average Rainfall'},
             title='Average Rainfall by Province')
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig)
        st.write(average_rain_by_province.T)

       
        
    elif option == 'Date':
        average_rain_by_date = df.groupby('date')['rain'].mean().reset_index()
        fig = px.line(average_rain_by_date, x='date', y='rain', 
             labels={'date':'Date', 'rain':'Average Rainfall'},
             title='Average Rainfall by Date')
        st.plotly_chart(fig)
        st.write(average_rain_by_date.T)

        
#second part
st.write('\n')
st.header('Column 2: Map raining in each area')
layer = pdk.Layer(
    'ScatterplotLayer',  # Type of layer
    df,  # DataFrame
    get_position='[longitude, latitude]',  # Position of each point
    get_radius='rain * 200',  # Size of each point
    get_fill_color='[200, 30, 0, 160]',  # Color of each point
    pickable=True,  # Enable hover effects
    auto_highlight=True  # Enable highlight effects
)

# Set the map's initial viewport
view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=6,
    pitch=0
)

# Render the map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Summary report
summary = df.describe()
summary_report = f"""
The dataset contains {len(df)} rows. The average rainfall is {summary.loc['mean', 'rain']:.2f} units, with a standard deviation of {summary.loc['std', 'rain']:.2f} units. The minimum rainfall recorded is {summary.loc['min', 'rain']:.2f} units, and the maximum is {summary.loc['max', 'rain']:.2f} units. The 25th percentile of rainfall is {summary.loc['25%', 'rain']:.2f} units, the median is {summary.loc['50%', 'rain']:.2f} units, and the 75th percentile is {summary.loc['75%', 'rain']:.2f} units.
"""
st.write('\n')
st.header('Summary Report')
st.write(summary_report)

# Code
st.write('\n')
st.header('Code')
with st.expander("## Code"):
    with open('rain_daily_6431345221.py', 'r') as file:
        code = file.read()
    st.code(code)
    
    
    