import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score # import cross_val_score function
import joblib
import pandas as pd
import numpy as np
from sklearn import tree # import tree function
import matplotlib.pyplot as plt
import pydotplus # import pydotplus package

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
# 导出随机森林中的一棵树为dot文件
num_tree = st.slider('Select one tree to demonstrate', 0, 19, 1)
tree_dot = tree.export_graphviz(rf.estimators_[num_tree], # choose one tree from the random forest model
                                out_file=None, # do not write to a file
                                feature_names=X.columns, # use the feature names as labels
                                class_names=['Not severe', 'Severe'], # use the class names as labels
                                filled=True) # fill the nodes with colors

st.graphviz_chart(tree_dot)

rf.feature_importances_.argsort()
plt.barh(df.feature_names[sorted_idx], rf.feature_importances_[sorted_idx])
plt.xlabel("Random Forest Feature Importance")
