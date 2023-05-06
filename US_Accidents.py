import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import datetime
import json
import folium
from streamlit_folium import st_folium

st.header("US Accidents Visulization")
st.write("Jiyan CHEN&emsp;&emsp;Leqi LIU&emsp;&emsp;Xiaoyu FU&emsp;&emsp;Linjie XIA")
st.markdown("<hr />", unsafe_allow_html=True)
"""
# EDA on US Accidents
## Overview of the data set
"""

with st.expander("Details about features used in the dataset"):
    st.write("""  
###### **Traffic Attributes (6):**
- **Severity:** Shows the severity of the accident, a number between 1 and 4, where 1 indicates the least impact on traffic (i.e., short delay as a result of the accident) and 4 indicates a significant impact on traffic (i.e., long delay).    
- **Start_Time:** Shows start time of the accident in local time zone.  
- **End_Time:** Shows end time of the accident in local time zone.  
- **Start_Lat:** Shows latitude in GPS coordinate of the start point.  
- **Start_Lng:** Shows longitude in GPS coordinate of the start point.  
- **Distance(mi):** The length of the road extent affected by the accident.  
###### **Address Attributes (6):**
- **Street:** Shows the street name in address field.
- **Side:** Shows the relative side of the street (Right/Left) in address field.
- **City:** Shows the city in address field.
- **County:** Shows the county in address field.
- **State:** Shows the state in address field.
- **Zipcode:** Shows the zipcode in address field.
###### **Weather Attributes (9):**
- **Temperature(F):** Shows the temperature (in Fahrenheit).
- **Wind_Chill(F):** Shows the wind chill (in Fahrenheit).
- **Humidity(%):** Shows the humidity (in percentage).
- **Pressure(in):** Shows the air pressure (in inches).
- **Visibility(mi):** Shows visibility (in miles).
- **Wind_Direction:** Shows wind direction.
- **Wind_Speed(mph):** Shows wind speed (in miles per hour).
- **Precipitation(in):** Shows precipitation amount in inches, if there is any.
- **Weather_Condition:** Shows the weather condition (rain, snow, thunderstorm, fog, etc.).
###### **POI Attributes (13):**
- **Amenity:** A Point-Of-Interest (POI) annotation which indicates presence of amenity in a nearby location.
- **Bump:** A POI annotation which indicates presence of speed bump or hump in a nearby location.
- **Crossing:** A POI annotation which indicates presence of crossing in a nearby location.
- **Give_Way:** A POI annotation which indicates presence of give_way sign in a nearby location.
- **Junction:** A POI annotation which indicates presence of junction in a nearby location.
- **No_Exit:** A POI annotation which indicates presence of no_exit sign in a nearby location.
- **Railway:** A POI annotation which indicates presence of railway in a nearby location.
- **Roundabout:** A POI annotation which indicates presence of roundabout in a nearby location.
- **Station:** A POI annotation which indicates presence of station (bus, train, etc.) in a nearby location.
- **Stop:** A POI annotation which indicates presence of stop sign in a nearby location.
- **Traffic_Calming:** A POI annotation which indicates presence of traffic_calming means in a nearby location.
- **Traffic_Signal:** A POI annotation which indicates presence of traffic_signal in a nearby location.
- **Turning_Loop:** A POI annotation which indicates presence of turning_loop in a nearby location.
###### **Period-of-Day (1):**
- **Sunrise_Sunset:** Shows the period of day (i.e. day or night) based on sunrise/sunset.
    """)

st.session_state['uploaded_file'] = st.file_uploader("Choose a file",key="data")
uploaded_file = st.session_state['uploaded_file']
if uploaded_file is not None:
    df = pd.read_feather(uploaded_file)
else:
    st.stop()