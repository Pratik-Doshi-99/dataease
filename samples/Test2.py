#Sample python file (manually created) to serve as reference for target Python output file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

auto1 = pd.read_csv('auto-mpg (1).csv')

print(auto1.head(10))

auto1 = auto1.drop('car name', axis=1)

auto1['horsepower'] = auto1['horsepower'].fillna(auto1['horsepower'].median())

sns.pairplot(auto1[["acceleration","weight","horsepower","displacement","cylinders","mpg"]], diag_kind='kde')

auto1_Y = auto1[['mpg']]
auto1_X = auto1.drop('mpg', axis = 1)
auto1_X_train, auto1_X_test, auto1_Y_train, auto1_Y_test = train_test_split(auto1_X,auto1_Y,test_size=0.2)

regModels_linreg = LinearRegression()
regModels_linreg.fit(auto1_X_train,auto1_Y_train)

# Evaluate the model
auto1_Y_pred = regModels_linreg.predict(auto1_X_test)
regModels_linreg_mse = mean_squared_error(auto1_Y_test, auto1_Y_pred)
regModels_linreg_r2 = r2_score(auto1_Y_test, auto1_Y_pred)

print('R2 Score (Test)',regModels_linreg_r2)
print('MSE (Test)',regModels_linreg_mse)