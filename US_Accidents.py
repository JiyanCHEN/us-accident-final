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
st.write("Jiyan CHEN")
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

if 'uploaded_file' in st.session_state:
    df = pd.read_feather(st.session_state.uploaded_file)
else:
    st.stop()
df = df.dropna().reset_index(drop=True)
df['Severity'] = df['Severity'].astype(np.int8)
st.write("*The following table shows the first 5 data:*")
st.write(df.head(5))
st.markdown("<hr />", unsafe_allow_html=True)
df['Year'] = pd.DatetimeIndex(df['Start_Time']).year
df["Month"] = pd.to_datetime(df["Start_Time"]).dt.month
df["Hour"] = pd.to_datetime(df["Start_Time"]).dt.hour

@st.cache_data
def draw_bar(df, x, y, c, log=False):
    fig_df = df.groupby([x, c])[y].count().reset_index()
    fig = px.bar(
        fig_df, y=y, x=x,
        text_auto='.2s', color=c,
        labels={x: x, y: "Accidents"},
        log_y=log
    )
    return fig
y = draw_bar(df, "Year", "State", "Severity", True)
m = draw_bar(df, "Month", "State", "Severity")
h = draw_bar(df, "Hour", "State", "Severity")


st.write("## Visulization on Accidents' Time Distribution")
period = st.radio(
    "Time distribution of accidents",
    ["Yearly", "Monthly", "Weekday", "Hourly"],
    label_visibility="collapsed",
    horizontal=True
)

if period == 'Yearly':
    st.plotly_chart(y)
elif period == 'Monthly':
    st.plotly_chart(m)
elif period == 'Weekday':
    pass
elif period == 'Hourly':
    st.plotly_chart(h)


st.write("---")
st.write("## Visulization on Accidents' Geo Distribution")
st.write("### 2016 - 2019 US Traffic Accident Dataset by State")
state_count_acc = pd.value_counts(df['State'])
fig_state = go.Figure(data=go.Choropleth(
    locations=state_count_acc.index,
    z=state_count_acc.values.astype(float),
    locationmode='USA-states',
    colorscale='Reds',
    colorbar_title='Count Accidents',
))
fig_state.update_layout(
    geo_scope='usa',
)
st.plotly_chart(fig_state)

st.write("### 2016 - 2019 US Traffic Accident Dataset by Counties")

fips = pd.read_csv("data/national_county.txt", header=None, names=[
                   "state_abb", "state_fips", "county_fips", "county_name", "class_code"], dtype={"state_fips": str, "county_fips": str})
fips["FIPS"] = fips.apply(lambda x: x["state_fips"] + x["county_fips"], axis=1)
fips["county_name"] = fips["county_name"].str.replace(" County", "")
accidents_by_county = df.groupby("County")["City"].count().reset_index()
accidents_by_county.columns = ["County", "accidents"]
result = pd.merge(accidents_by_county, fips[[
                  "county_name", "state_fips", "county_fips", "FIPS"]], left_on="County", right_on="county_name")
result = result[["County", "state_fips", "county_fips", "FIPS", "accidents"]]

with open("geojson-counties-fips.json") as f:
    counties = json.load(f)

fig = px.choropleth_mapbox(result, geojson=counties, locations='FIPS', color='accidents',
                           color_continuous_scale="orrd",
                           mapbox_style="carto-positron",
                           zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           hover_data=["County", "accidents"]
                           )

st.plotly_chart(fig)


st.write("### Scatter map")
st.write('The following map shows the cluster of accidents during the selected period')


def get_color(severity):
    if severity == 1:
        return "green"
    elif severity == 2:
        return "yellow"
    elif severity == 3:
        return "orange"
    else:
        return "red"

@st.cache_resource
def create_map(df, start_date, end_date):
    s = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    marker_cluster = folium.plugins.MarkerCluster()
    df_filtered = df[(df["Start_Time"] >= pd.to_datetime(start_date)) & (
        df["Start_Time"] <= pd.to_datetime(end_date))]
    for index, row in df_filtered.iterrows():
        folium.CircleMarker(
            location=[row["Start_Lat"], row["Start_Lng"]],
            radius=5,
            color=get_color(row["Severity"]),
            fill=True,
            fill_color=get_color(row["Severity"]),
            fill_opacity=0.5,
            popup=folium.Popup(
                f"Date: {row['Start_Time']}<br>Severity: {row['Severity']}<br>Latitude :{row['Start_Lat']}<br>Longitude:{row['Start_Lat']}<br>Side:{row['Side']}<br>Weather:{row['Weather_Condition']}<br>Period of Day:{row['Sunrise_Sunset']}")
        ).add_to(marker_cluster)
    marker_cluster.add_to(s)
    return s


start_date, end_date = st.date_input("Select the period", value=[datetime.date(2017, 1, 1), datetime.date(
    2017, 2, 1)], min_value=datetime.date(2016, 1, 1), max_value=datetime.date(2020, 12, 31))

st_data = st_folium(create_map(df, start_date, end_date),
                    width=720, height=480)

"""
## Correlation Analysis
"""
