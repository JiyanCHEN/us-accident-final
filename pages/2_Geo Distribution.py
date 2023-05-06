import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import datetime
import json
import folium
from streamlit_folium import st_folium

if st.session_state['uploaded_file'] is None:
    st.warning("Please upload the dataset first")
    st.stop()
    
uploaded_file = st.session_state.uploaded_file
df = pd.read_feather(uploaded_file)
df = df.dropna().reset_index(drop=True)
df['Severity'] = df['Severity'].astype(np.int8)

st.markdown("<hr />", unsafe_allow_html=True)
df['Year'] = pd.DatetimeIndex(df['Start_Time']).year
df["Month"] = pd.to_datetime(df["Start_Time"]).dt.month
df["Hour"] = pd.to_datetime(df["Start_Time"]).dt.hour

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
