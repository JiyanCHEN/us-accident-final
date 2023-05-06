import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score # import cross_val_score function
import joblib
import pandas as pd
import numpy as np

df = pd.read_feather(st.session_state.uploaded_file)
df = df.dropna()
df['Severity']=df['Severity'].astype(np.int8)
df["is_severe"]= np.where(df['Severity'] == 4, 1, 0)

@cache_resource
def read_model(model):
    model = joblib.load(model)
    return model

# 选择目标变量
y = df["is_severe"]
# 选择特征变量
X = df[['Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 
        'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 
        'Precipitation(in)', 'Amenity', 'Bump', 'Crossing', 
        'Give_Way', 'Junction', 'No_Exit', 'Railway', 'Roundabout', 
        'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal']]
# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=202355)
scores = cross_val_score(rf, X, y, cv=10) # use 10-fold cross-validation
st.write("Cross-validation scores:", scores)
st.write("Mean score:", scores.mean())
st.write("Standard deviation:", scores.std())

