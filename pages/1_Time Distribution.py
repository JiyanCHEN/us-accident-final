import streamlit as st
import plotly.express as px
import pandas as pd
uploaded_file = st.session_state.uploaded_file
df = pd.read_feather(uploaded_file)
df = df.dropna().reset_index(drop=True)
df['Severity'] = df['Severity'].astype(np.int8)
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
    