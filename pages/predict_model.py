import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score # import cross_val_score function
import joblib
import pandas as pd
import numpy as np

if 'uploaded_file' not in st.session_state:
    st.warning("Please upload the dataset first")
    st.stop()

uploaded_file = st.session_state.uploaded_file
df = pd.read_feather(uploaded_file)
df = df.dropna()
df['Severity']=df['Severity'].astype(np.int8)
df["is_severe"]= np.where(df['Severity'] == 4, 1, 0)

y = df["is_severe"]
X = df[['Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 
        'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 
        'Precipitation(in)', 'Amenity', 'Bump', 'Crossing', 
        'Give_Way', 'Junction', 'No_Exit', 'Railway', 
        'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal']]

@st.cache_resource
def read_model(model):
    model = joblib.load(model)
    return model

rf=read_model('RandomForestClassifier.m')

features = ['Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 
        'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 
        'Precipitation(in)', 'Amenity', 'Bump', 'Crossing', 
        'Give_Way', 'Junction', 'No_Exit', 'Railway', 
        'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal']

# Create a dictionary to store the values of the features
values = {}

# Create a form with a key
with st.form(key="my_form"):
    # Loop through the features and create input widgets for each feature
    for feature in features:
        # If the feature is a boolean, use a checkbox widget
        if feature in ['Amenity', 'Bump', 'Crossing', 
        'Give_Way', 'Junction', 'No_Exit', 'Railway', 
        'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal']:
            values[feature] = st.checkbox(feature)
        # Otherwise, use a number input widget
        else:
            values[feature] = st.number_input(feature)
    # Create a submit button
    submit = st.form_submit_button(label="Submit")

# If the form is submitted, display the values of the features
if submit:
    input = pd.DataFrame(values, index=[0])
    predict = rf.predict(input)
    st.write(predict)
