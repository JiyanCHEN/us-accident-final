from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score # import cross_val_score function
import matplotlib.pyplot as plt # import matplotlib.pyplot module

# 读取数据集
import pandas as pd
import numpy as np
df = pd.read_feather('data/data212979/US_Accidents.feather')
df = df.dropna()
df['Severity']=df['Severity'].astype(np.int8)
df["is_severe"]= np.where(df['Severity'] == 4, 1, 0)

# 选择目标变量
y = df["is_severe"]

# 选择特征变量
X = df[['Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 'Precipitation(in)', 'Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit', 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal']]

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=202355)

# 创建随机森林回归器

rf = RandomForestClassifier(n_estimators=20, max_depth=6, criterion="gini")

# 训练模型
rf.fit(X_train, y_train)

# 使用交叉验证评估模型性能
scores = cross_val_score(rf, X, y, cv=10) # use 10-fold cross-validation
print("Cross-validation scores:", scores)
print("Mean score:", scores.mean())
print("Standard deviation:", scores.std())