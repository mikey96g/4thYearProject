import numpy
import matplotlib.pyplot as plt
import pandas
import math
import schedule
from keras.models import Sequential,load_model
from keras.layers import Dense, LSTM, Dropout,Activation
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import pyodbc
import pandas as pd
import datetime
import time as t

# convert an array of values into a dataset matrix


def create_dataset(dataset, window_size=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - window_size - 1):
        a = dataset[i:(i + window_size), :]
        dataX.append(a)
        dataY.append(dataset[i + window_size, 0])
    return numpy.array(dataX), numpy.array(dataY)



# fix random seed for reproducibility
numpy.random.seed(7)


cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
							  ';Server=tcp:year4bitcoin.database.windows.net,1433;'
							  'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
							  'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()
def create_Model():
	# fix random seed for reproducibility
	numpy.random.seed(7)



	sql = "select sentVal from dbo.SentimentValues"
	sql3 = "select sentTotal from dbo.SentimentValues"
	sql2 = "select closePrice,openingPrice,highPrice,lowPrice,bandUpper,bandLower,volCoin ,volEuro from dbo.BitcoinVal"

	df = pd.read_sql(sql,cnxn)
	df2 = pd.read_sql(sql2,cnxn)
	df3 = pd.read_sql(sql3,cnxn)
	# print(df3.head())
	dfv = df.values
	dft = df3.values
	df2['sentVal'] = dfv
	df2['sentTotal']=dft
	dataset =df2
	# print(dataset.head())

	# normalize the dataset
	scaler = MinMaxScaler(feature_range=(-1, 1))
	dataset = scaler.fit_transform(dataset)
	d2 =dataset
	# split into train and test sets
	train_size = int(len(dataset) * 0.80) 
	test_size = len(dataset) - train_size
	train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

	# reshape into X=t and Y=t+1
	window_size = 24
	trainX, trainY = create_dataset(train, window_size)  
	testX, testY = create_dataset(test, window_size)

	# reshape input to be  [samples, time steps, features] for Sequential model
	trainX = numpy.reshape(trainX, (trainX.shape[0], window_size, 10))
	testX = numpy.reshape(testX, (testX.shape[0],window_size, 10))

	# create and fit the LSTM network
	model = Sequential()
	model.add(LSTM(input_shape = (window_size,10), output_dim= 10,return_sequences=True))
	model.add(Dropout(0.2))
	model.add(LSTM(100))
	model.add(Dropout(0.5))
	model.add(Dense(1))
	model.add(Activation('tanh'))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.summary()
	history= model.fit(trainX, trainY,validation_split=0.20, nb_epoch=205, batch_size=32)

	# make predictions
	trainPredict = model.predict(trainX)
	testPredict = model.predict(testX)


	# renormalising the data 
	trainPredict_extended = numpy.zeros((len(trainPredict),10))
	trainPredict_extended[:,0] = trainPredict[:,0]
	trainPredict = scaler.inverse_transform(trainPredict_extended) [:,0]  


	testPredict_extended = numpy.zeros((len(testPredict),10))
	testPredict_extended[:,0] = testPredict[:,0]
	testPredict = scaler.inverse_transform(testPredict_extended)[:,0]   

	trainY_extended = numpy.zeros((len(trainY),10))
	trainY_extended[:,0]=trainY
	trainY=scaler.inverse_transform(trainY_extended)[:,0]

	testY_extended = numpy.zeros((len(testY),10))
	testY_extended[:,0]=testY
	testY=scaler.inverse_transform(testY_extended)[:,0]

	#calculate root mean squared error
	trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
	print('Train Score: %.2f RMSE' % (trainScore))
	testScore = math.sqrt(mean_squared_error(testY, testPredict))
	print('Test Score: %.2f RMSE' % (testScore))

	multiN = testPredict[-1]
	sentN = create_Model2()
	
	date = datetime.datetime.now().date()
	time = datetime.datetime.now().time()
	ds = datetime.datetime.now()
	cursor.execute("INSERT INTO dbo.results "
					    "(lstmSent,lstmMulti,rTime,rDate,timeDate)"
					    " values(?,?,?,?,?)", sentN,multiN,time, date,ds)
	cnxn.commit() 
	print(multiN)
	print(sentN)

	return   multiN


def create_Model2():
	sql = "select sentVal , sentTotal from dbo.SentimentValues"
	sql2 = "select closePrice from dbo.BitcoinVal"

	df = pd.read_sql(sql,cnxn)
	df2 = pd.read_sql(sql2,cnxn)
	dfa = df2.values
	df['ClosingPrice'] = dfa
	dataset =df


	# normalize the dataset
	scaler = MinMaxScaler(feature_range=(-1, 1))
	dataset = scaler.fit_transform(dataset)

	# split into train and test sets
	train_size = int(len(dataset) * 0.80) 
	test_size = len(dataset) - train_size
	train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

	# reshape into X=t and Y=t+1
	window_size = 24
	trainX, trainY = create_dataset(train, window_size)  
	testX, testY = create_dataset(test, window_size)

	# reshape input to be  [samples, time steps, features] for Sequential model
	trainX = numpy.reshape(trainX, (trainX.shape[0], window_size, 3))
	testX = numpy.reshape(testX, (testX.shape[0],window_size, 3))

	# create and fit the LSTM network
	model = Sequential()
	model.add(LSTM(input_shape = (24,3), output_dim= 3,return_sequences=True))
	model.add(Dropout(0.2))
	model.add(LSTM(100))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.summary()
	history= model.fit(trainX, trainY,validation_split=0.20, nb_epoch=210, batch_size=30)

	# make predictions
	trainPredict = model.predict(trainX)
	testPredict = model.predict(testX)

	# renormalising the data 
	trainPredict_extended = numpy.zeros((len(trainPredict),3))
	trainPredict_extended[:,2] = trainPredict[:,0]
	trainPredict = scaler.inverse_transform(trainPredict_extended) [:,2]  


	testPredict_extended = numpy.zeros((len(testPredict),3))
	testPredict_extended[:,2] = testPredict[:,0]
	testPredict = scaler.inverse_transform(testPredict_extended)[:,2]   

	trainY_extended = numpy.zeros((len(trainY),3))
	trainY_extended[:,2]=trainY
	trainY=scaler.inverse_transform(trainY_extended)[:,2]

	testY_extended = numpy.zeros((len(testY),3))
	testY_extended[:,2]=testY
	testY=scaler.inverse_transform(testY_extended)[:,2]


	# calculate root mean squared error
	trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
	print('Train Score: %.2f RMSE' % (trainScore))
	testScore = math.sqrt(mean_squared_error(testY, testPredict))
	print('Test Score: %.2f RMSE' % (testScore))
	
	sentN = testPredict[-1]
	
	return sentN
	
multiN = create_Model()
#sentN = create_Model2()
#print(multiN)
#print(sentN)

schedule.every(5).minutes.do(create_Model)
#schedule.every(5).minutes.do(create_Model2)



while True:
    schedule.run_pending()
    t.sleep(1)


cnxn.close()






