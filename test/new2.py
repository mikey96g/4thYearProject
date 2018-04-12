import pyodbc
import pandas as pd
import numpy as np

cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                          ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                          'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                          'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()

sql = "select sentVal , sentTotal from dbo.SentimentValues"
sql2 = "select closePrice from dbo.BitcoinVal"

df = pd.read_sql(sql,cnxn)
df2 = pd.read_sql(sql2,cnxn)
dfa = df2.values
df['ClosingPrice'] = dfa
print(len(dfa))
