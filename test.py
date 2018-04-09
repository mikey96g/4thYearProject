import pyodbc
import pandas as pd
import numpy as np
#np.show_config()
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
# fix random seed for reproducibility
np.random.seed(7)

#Sorting data into x and x+1
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), :]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                      ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                      'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                      'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


					  
def load_data():
	sql = "Select * from dbo.BitcoinVal"
	df = pd.read_sql(sql,cnxn)

	df_stock = df.copy()
	df_stock.drop(['dboTime'],1,inplace=True)
	df_stock.drop(['timeDate'],1,inplace=True)
	df_stock.drop(['dateTimeS'],1,inplace=True)
	df_stock.drop(['dateB'],1,inplace=True)
	df_stock.drop(['bandUpper'],1,inplace=True)
	df_stock.drop(['bandLower'],1,inplace=True)

	# normalize the dataset
	scaler = MinMaxScaler(feature_range=(0, 1))
	dataset = scaler.fit_transform(df_stock)
	train_size = int(len(dataset) * 0.8)
	test_size = len(dataset) - train_size
	train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
	print(len(train), len(test))

	# reshape into X=t and Y=t+1
	look_back = 1
	trainX, trainY = create_dataset(train, look_back)
	testX, testY = create_dataset(test, look_back)
	
	# reshape input to be [samples, time steps, features]
	trainX = np.reshape(trainX, (trainX.shape[0], look_back, 6))
	testX = np.reshape(testX, (testX.shape[0], look_back, 6))
	
	return trainX ,trainY,testX, testY


def create Model()	
	# create and fit the LSTM network
	model = Sequential()
	model.add(LSTM(4, input_shape=(look_back,6)))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model
	
history= model.fit(trainX, trainY,validation_split=0.33, nb_epoch=100, batch_size=10)


trainX ,trainY,testX, testY= load_data()

#make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# Get something which has as many features as dataset
trainPredict_extended = np.zeros((len(trainPredict),6))
# Put the predictions there
trainPredict_extended[:,5] = trainPredict[:,0]
# Inverse transform it and select the 3rd column.
trainPredict = scaler.inverse_transform(trainPredict_extended) [:,1]  

# Get something which has as many features as dataset
testPredict_extended = np.zeros((len(testPredict),6))
# Put the predictions there
testPredict_extended[:,5] = testPredict[:,0]
# Inverse transform it and select the 2nd column.
testPredict = scaler.inverse_transform(testPredict_extended) [:,1]  


trainY_extended = np.zeros((len(trainY),6))
trainY_extended[:,5]=trainY
trainY=scaler.inverse_transform(trainY_extended)[:,1]


testY_extended = np.zeros((len(testY),6))
testY_extended[:,5]=testY
testY=scaler.inverse_transform(testY_extended)[:,1]


trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, 1] = trainPredict

print(testY[0])

# calculate root mean squared error
#trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
#print('Train Score: %.2f RMSE' % (trainScore))
#testScore = math.sqrt(mean_squared_error(testY, testPredict))
#print('Test Score: %.2f RMSE' % (testScore))


# Plot training
#plt.plot(history.history['loss'])
#plt.plot(history.history['val_loss'])
#plt.title('model loss')
#plt.ylabel('lost')
#plt.xlabel('time')
#plt.legend(['training', 'validation'], loc='upper right')
#plt.show()



