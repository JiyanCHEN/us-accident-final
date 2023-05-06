import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score # import cross_val_score function
import joblib
import pandas as pd
import numpy as np
from IPython.display import Image # import Image function
from sklearn import tree # import tree function
import pydotplus # import pydotplus package

uploaded_file = st.session_state.uploaded_file
df = pd.read_feather(uploaded_file)
df = df.dropna()
df['Severity']=df['Severity'].astype(np.int8)
df["is_severe"]= np.where(df['Severity'] == 4, 1, 0)

@st.cache_resource
def read_model(model):
    model = joblib.load(model)
    return model

rf=read_model('RandomForestClassifier.m')
# 导出随机森林中的一棵树为dot文件
tree = st.slider('Select one tree to demonstrate', 0, 19, 1)
tree_dot = tree.export_graphviz(rf.estimators_[tree], # choose one tree from the random forest model
                                out_file=None, # do not write to a file
                                feature_names=X.columns, # use the feature names as labels
                                class_names=['Not severe', 'Severe'], # use the class names as labels
                                filled=True) # fill the nodes with colors

st.graphviz_chart(tree_dot)

