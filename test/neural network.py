import pyodbc
import pandas as pd
import numpy as np
import numpy
import matplotlib.pyplot as plt
import pandas
import math
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                      ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                      'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                      'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

sql = "Select * from dbo.BitcoinVal, Order BY date,time"
df = pd.read_sql(sql,cnxn)

df_stock = df.copy()
df_stock.drop(['dboTime'],1,inplace=True)
df_stock.drop(['timeDate'],1,inplace=True)
df_stock.drop(['dateTimeS'],1,inplace=True)
df_stock.drop(['dateB'],1,inplace=True)
df_stock.drop(['bandUpper'],1,inplace=True)
df_stock.drop(['bandLower'],1,inplace=True)

print(df_stock.head())