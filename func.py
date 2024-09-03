import pickle
import numpy as np 
import pandas as pd 


from sklearn.preprocessing import MinMaxScaler
df = pd.read_csv('rice.csv')
df1 = df.drop(columns=['Date'])
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(np.array(df1).reshape(-1,1))

pickle_in  = open("proj1/rice.pkl" , "rb")
model = pickle.load(pickle_in)

days =1  

def prediction(days, dataset):
    arr = np.array(dataset[-120:])
    output = []
    for i in range(days):
        forecast = model.predict(arr.reshape(-1, 1))  # ensure shape is (120, 1)
        forecast = scaler.inverse_transform(forecast)[0][0]  # extract the single value
        arr = np.roll(arr, -1)  # shift the array to make room for the new value
        arr[-1] = forecast  # add the new value to the end of the array
        output.append(forecast)
    return output
forecast = prediction(3, df1)
print(forecast)

    



