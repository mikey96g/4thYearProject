import pyodbc
import json
import datetime


from apscheduler.schedulers.background import BackgroundScheduler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import requests


#consumer key, consumer secret, access token, access secret.
ckey=''
csecret=''import pyodbc
import json
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import requests
import numpy as np


#consumer key, consumer secret, access token, access secret.
ckey=''
csecret=''
atoken=''
asecret=''


#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:year4bitcoin.database.windows.net,1433;Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()


analyzer = SentimentIntensityAnalyzer()
#List for storing values
vs_compound = []

# Start the scheduler
sched = BackgroundScheduler()

class listener(StreamListener):



    def on_data(self, data):

        all_data = json.loads(data)
        try:
            tweet = all_data["text"]
            if 'RT @' not in tweet:
                vs = analyzer.polarity_scores(tweet)
                vs_compound.append(analyzer.polarity_scores(tweet)['compound'])

        except KeyError:
            'text'

        return(True)


    def on_error(self, status):
        print('There is an error', status)


def sent_Avg():

    avg = sum(vs_compound)/len(vs_compound)
    vs_compound.clear()
    dTime = datetime.datetime.now()
    dateS = datetime.datetime.now().date()
    dateT = datetime.datetime.now().time()
    cursor.execute("INSERT INTO dbo.sentimentValues (sentVal,dateS,timeS,dateTimeS) values(?,?,?,?)",avg,dateS,dateT,dTime)
    cnxn.commit()


    print(avg)


def btc_call():
    req = requests.get('https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=0&aggregate=1&e=CCCAGG')
    close = req.json()['Data'][0]['close']
    open = req.json()['Data'][0]['open']
    high = req.json()['Data'][0]['high']
    low = req.json()['Data'][0]['low']
    bitVolume = req.json()['Data'][0]['volumefrom']
    dollarVol = req.json()['Data'][0]['volumeto']
    dTime = datetime.datetime.now()
    dateS = datetime.datetime.now().date()
    dateT = datetime.datetime.now().time()
    cursor.execute("INSERT INTO dbo.BitcoinVal (CLOSEPRICE,DATEB,TIMEB,dateTimeB) values(?,?,?,?)", close, dateS,
                   dateT, dTime)
    cnxn.commit()
    print(close)

def bollinger_band():
    req = requests.get('https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=0&aggregate=1&e=CCCAGG')
    close = req.json()['Data'][0]['close']
    holdVal = []
    holdVal.insert(0,close)
    if len(holdVal) == 6:
        holdVal.pop(5)
    sma = sum(holdVal)/len(holdVal)
    deviation = np.std(holdVal)*2
    upper = sma + deviation
    lower = sma - deviation
    print(upper)
    print(lower)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


sched.add_job(sent_Avg,'interval',seconds=60)
sched.add_job(btc_call, 'interval', seconds=60)
sched.add_job(bollinger_band, 'interval', seconds=60)


sched.start()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Bitcoin"])
cnxn.close()




atoken=''
asecret=''


#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:projdata.database.windows.net,1433;Database=projData;Uid=mikey96g@projdata;Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()


analyzer = SentimentIntensityAnalyzer()
#List for storing values
vs_compound = []

# Start the scheduler
sched = BackgroundScheduler()

class listener(StreamListener):



    def on_data(self, data):

        all_data = json.loads(data)
        try:
            tweet = all_data["text"]
            if 'RT @' not in tweet:
                vs = analyzer.polarity_scores(tweet)
                vs_compound.append(analyzer.polarity_scores(tweet)['compound'])

        except KeyError:
            'text'

        return(True)


    def on_error(self, status):
        print('There is an error', status)


def sent_Avg():

    avg = sum(vs_compound)/len(vs_compound)
    vs_compound.clear()
    dTime = datetime.datetime.now()
    dateS = datetime.datetime.now().date()
    dateT = datetime.datetime.now().time()
    cursor.execute("INSERT INTO dbo.sentimentValues (sentVal,dateS,timeS,dateTimeS) values(?,?,?,?)",avg,dateS,dateT,dTime)
    cnxn.commit()


    print(avg)


def btc_call():
    req = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    price = req.json()['bpi']['USD']['rate']
    dTime = datetime.datetime.now()
    dateS = datetime.datetime.now().date()
    dateT = datetime.datetime.now().time()
    cursor.execute("INSERT INTO dbo.BitcoinVal (BCOINCLOSE,DATEB,TIMEB,dateTimeB) values(?,?,?,?)", price, dateS,
                   dateT, dTime)
    cnxn.commit()
    print(price)




auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


sched.add_job(sent_Avg,'interval',seconds=60)
sched.add_job(btc_call, 'interval', seconds=60)

sched.start()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Bitcoin"])
cnxn.close()



