import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                      ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                      'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                      'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

sql = "Select * from dbo.BitcoinVal"
df = pd.read_sql(sql,cnxn)
plt.plot(df)
plt.show()