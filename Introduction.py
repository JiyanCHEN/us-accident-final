import streamlit as st
import pandas as pd


st.title("US Accidents Visulization")
st.write("Jiyan CHEN&emsp;&emsp;Leqi LIU&emsp;&emsp;Xiaoyu FU&emsp;&emsp;Linjie XIA")
st.markdown("<hr />", unsafe_allow_html=True)
"""
## Background
Traffic accidents are one of the leading causes of death and injury worldwide. According to the World Health Organization, around 1.35 million people die in road accidents every year, and an additional 20-50 million suffer non-fatal injuries, which can have a profound impact on their lives. While there are various factors that contribute to the occurrence of traffic accidents, visual analysis of the data can provide valuable insights into their causes and patterns.

In recent years, Internet of Things (IoT)has developed rapidly, and improves the data collecting of traffic accidents. One of the benefits of the IoT is that it enables the collection and analysis of data from various sources in real time. This can be especially useful for improving the management and prevention of traffic accidents. By using sensors, cameras, GPS, and other devices, IoT can provide detailed information about the location, speed, direction, and condition of vehicles involved in accidents. This data can help authorities to respond faster, identify the causes, and reduce the impacts of collisions. Moreover, IoT can also help drivers to avoid accidents by providing them with alerts, warnings, and recommendations based on the data collected from other vehicles and road infrastructure. Therefore, the development of IoT can improve the data collecting of traffic accidents and enhance the safety and efficiency of transportation systems.
"""
"""
## Overview of the data set
The dataset for this research comes from Kaggle, it is a countrywide car accident dataset, which covers 49 states of the USA. The accident data are collected from February 2016 to Dec 2021, using multiple APIs that provide streaming traffic incident (or event) data. These APIs broadcast traffic data captured by a variety of entities, such as the US and state departments of transportation, law enforcement agencies, traffic cameras, and traffic sensors within the road-networks.
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

st.divider()
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if st.session_state['uploaded_file'] is None:
    st.session_state['uploaded_file'] = st.file_uploader("Choose a file",key="data")
uploaded_file = st.session_state['uploaded_file']
if uploaded_file is not None:
    df = pd.read_feather(uploaded_file)
else:
    st.stop()