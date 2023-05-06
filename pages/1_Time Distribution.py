import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
    
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
df["Weekday"] = pd.to_datetime(df["Start_Time"]).dt.weekday

@st.cache_data
def draw_bar(df, x, y, c, log=False):
    fig_df = df.groupby([x, c])[y].count().reset_index()
    fig = px.bar(
        fig_df, y=y, x=x,
        text_auto='.2s', color=c,
        color_discrete_sequence=['green','yellow','orange', 'red'],
        labels={x: x, y: "Accidents"},
        log_y=log
    )
    return fig

y = draw_bar(df, "Year", "State", "Severity", True)
m = draw_bar(df, "Month", "State", "Severity")
h = draw_bar(df, "Hour", "State", "Severity")
w = draw_bar(df, "Weekday", "State", "Severity")

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
    st.plotly_chart(w)
elif period == 'Hourly':
    st.plotly_chart(h)
    