# -*- coding: utf-8 -*-
"""
College admissions project
Predicting chance of university admission from various scores
Ed Hayter 20/05/20
dataset from: https://www.kaggle.com/mohansacharya/graduate-admissions
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, RANSACRegressor, HuberRegressor, TheilSenRegressor
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor, RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor 

#read csv file
path = 'C:\C Documents\Kaggle\College admissions\Admission_Predict_Ver1.1.csv'
data = pd.read_csv(path)
#check for missing data
print('missing data:\n', data.isnull().sum())

#plot some data, see if anything correlates well
# g = sns.pairplot(data)

#split dataset into train, validation sets
y = data['Chance of Admit '] 
x = data.drop(['Chance of Admit ','Serial No.'],axis=1)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

#set up regressors to test
regressors=[['Linear Regression',LinearRegression()],
       ['Decision Tree Regression',DecisionTreeRegressor(random_state=42)],
       ['Random Forest Regression',RandomForestRegressor(random_state=42)],
       ['Gradient Boosting Regression', GradientBoostingRegressor(random_state=42)],
       ['Ada Boosting Regression',AdaBoostRegressor(random_state=42)],
       ['Extra Tree Regression', ExtraTreesRegressor(random_state=42)],
       ['K-Neighbors Regression',KNeighborsRegressor()],
       ['Support Vector Regression',SVR()],
       ['XGBoost Regression',XGBRegressor(random_state=42)],
       ['RANSAC Regression',RANSACRegressor(random_state=42)],
       ['Huber Regression',HuberRegressor()],
       ['TheilSen Regression',TheilSenRegressor(random_state=42)]]

#loop over regressors
RMSE = dict()
for name, regressor in regressors:
    #set up pipeline to include scaling
    pipe = Pipeline([('scaler', StandardScaler()),
                     ('reg',regressor)
                     ])
    pipe.fit(x_train,y_train)
    rmse = np.sqrt(mean_squared_error(y_test,pipe.predict(x_test)))
    print(name,': ', rmse)
    RMSE[name] = rmse
    
#Plot RMSEs for each model
plt.figure()
sns.barplot(y=list(RMSE.keys()),x=list(RMSE.values()))
#Looks like ThielSen is working best, lets see what features are most important.
plt.figure()
sns.barplot(x.columns,pipe.named_steps['reg'].coef_)










