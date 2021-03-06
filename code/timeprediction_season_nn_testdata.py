# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:32:55 2018

@author: mansi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 18:47:53 2018

@author: mansi
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xlwt as xl
from sklearn.model_selection import KFold as kf
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers import Dense
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
#import seaborn as sns

#import matplotlib.pyplot as plt
#import seaborn as sns
seed = 5;
classification_reports = []
accuracies =[]
confusion_matrices = []
def date_time_converter(value):
    #if(isinstance(value, str)):
        date = pd.to_datetime(value, format='%m/%d/%Y')
        return date
def season_crime(month):
    if month in range(1,4):
        season="spring"
    elif month in range(4,7):
        season="summer"
    elif month in range(7,11):
        season="monsoon"
    elif month in range(11,13):
        season="winter"
    return season
    print(season)
def format_time(b):
    new_time = ''
    time = b
    if not time:
        return ''
    elif(len(time)==1):
        new_time = "0" +time + "00"
    elif(len(time)==2 and int(time)<24):
        new_time = time + "00"
    elif(len(time)==2 and int(time)>=24):
        new_time = "00" + time
    elif(len(time)==3):
        new_time = "0" + time
    elif(len(time) == 4):
        new_time = time
    final_time = new_time[0:2]
    return final_time

def crime_code(str1):
    return int(str1[0:1])
def isWeekday(day):
    if day in range(1,5):
        return 0
    else:
        return 1
def format_crime_code(str1):
    return int(str1[0:1])

df=pd.read_csv('D:/Sem1/INF552/Project/Data/Final1/train.csv',
               converters={'Date Occurred': date_time_converter,'Time Occurred':format_time,
                           'Crime Code': crime_code})  
#df=df[np.isfinite(df['Weapon Used Code'])]
columns = df.columns
b=df[['Date Occurred','Time Occurred','Crime Code', 'Area ID']]

a=type(columns)

column_1 = df.ix[:,3]
f=type(column_1)

b['weekday'] = column_1.dt.dayofweek
b['month'] = column_1.dt.month
b['isWeekend'] = b['weekday'].apply(isWeekday)
b['season']=b['month'].apply(season_crime)


b = pd.concat([b.get(['Time Occurred','Date Occurred','Crime Code','Area ID','weekday','month','isWeekend']),
                           pd.get_dummies(b['Time Occurred'], prefix='Hour'),
                           pd.get_dummies(b['Crime Code'], prefix='Crime'),
                           pd.get_dummies(b['Area ID'], prefix='Area'),
                           pd.get_dummies(b['weekday'], prefix='day'),
                           pd.get_dummies(b['month'], prefix='month'),
                           pd.get_dummies(b['isWeekend'], prefix = 'isWeekend'),
#                           pd.get_dummies(b['Weapon Used Code'], prefix='Weapon'),
                           pd.get_dummies(b['season'],prefix='season')],axis=1)

X = b.iloc[:,2:].values
Y = b.iloc[:,0].values
df1 = pd.read_csv('D:/Sem1/INF552/Project/Data/Final1/test_type.csv',converters={'Date Occurred': date_time_converter, 
                                            'Time Occurred': format_time,
                                            'Crime Code': format_crime_code})
columns = df.columns
b1=df[['Date Occurred','Time Occurred','Crime Code', 'Area ID']]
a=type(columns)
column_1 = df.ix[:,3]
f=type(column_1)
b1['weekday'] = column_1.dt.dayofweek
b1['month'] = column_1.dt.month
b1['isWeekend'] = b['weekday'].apply(isWeekday)
b1['season']=b['month'].apply(season_crime)
b1 = pd.concat([b1.get(['Time Occurred','Date Occurred','Crime Code','Area ID','weekday','month','isWeekend']),
                          pd.get_dummies(b['Time Occurred'], prefix='Hour'),
                          pd.get_dummies(b['Crime Code'], prefix='Crime'),
                          pd.get_dummies(b['Area ID'], prefix='Area'),
                          pd.get_dummies(b['weekday'], prefix='day'),
                          pd.get_dummies(b['month'], prefix='month'),
                          pd.get_dummies(b['isWeekend'], prefix = 'isWeekend'),
#pd.get_dummies(b['Weapon Used Code'], prefix='Weapon'),
                          pd.get_dummies(b['season'],prefix='season')],axis=1)
X_test = b.iloc[:,2:].values
y_test = b.iloc[:,0].values


model = Sequential()
model.add(Dense(150, input_dim=84, activation='relu'))
model.add(Dense(100, activation='tanh'))
#model.add(Flatten())
model.add(Dense(24, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

#divide training data into 10 pairs of train and dev
#kfn = kf(n_splits=10, random_state=5, shuffle=False)
#kfn.get_n_splits(X_full)


#from sklearn.model_selection import StratifiedKFold
#kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
accuracies = []
#for train, test in kfold.split(X_full, y_full):
#    model.fit(X_full[train], y_full[train], epochs=150, batch_size=10, verbose=0)
#    # evaluate the model
#    scores = model.evaluate(X_full[test], y_full[test], verbose=0)
#    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
#    accuracies.append(scores[1] * 100)





from sklearn.model_selection import train_test_split
X_train, X_dev, y_train, y_dev = train_test_split(X, Y, test_size=0.25, random_state=0)
model.fit(X_train, y_train, epochs=10, batch_size=10, verbose=1)
# evaluate the model


scores_train = model.evaluate(X_train, y_train, verbose=1)
print("%s: %.2f%%" % (model.metrics_names[1], scores_train[1]*100))
accuracies.append(scores_train[1] * 100)
print("%.2f%% (+/- %.2f%%)" % (np.mean(accuracies), np.std(accuracies)))


scores_dev = model.evaluate(X_dev, y_dev, verbose=1)
print("%s: %.2f%%" % (model.metrics_names[1], scores_dev[1]*100))
accuracies.append(scores_dev[1] * 100)
print("%.2f%% (+/- %.2f%%)" % (np.mean(accuracies), np.std(accuracies)))


scores_test = model.evaluate(X_test, y_test, verbose=1)
print("%s: %.2f%%" % (model.metrics_names[1], scores_test[1]*100))
accuracies.append(scores_test[1] * 100)
print("%.2f%% (+/- %.2f%%)" % (np.mean(accuracies), np.std(accuracies)))


print("********************************accuracies******************************")
print("Train: " + str(accuracies[0]))
print("Validation: " + str(accuracies[1]))
print("Test: " + str(accuracies[2]))
print("************************************************************************")




