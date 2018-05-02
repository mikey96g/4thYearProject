import pyodbc
import json
import datetime
import re

from apscheduler.schedulers.background import BackgroundScheduler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import requests
import statistics as stats
import numpy as np


#consumer key, consumer secret, access token, access secret.
ckey='IXO7y3NtUqgZcki3KuW1p4nS0'
csecret='t1MTUtlD1TMemTqpgRyOpzKn3oMIVj3F4Rjoc4mHJsQgUahmtG'
atoken='2705490329-80t7yqBWhTvOUAZy3VC4v9SvibbabU2MMsFZuHX'
asecret='u1s6637pHzvF1aHWejgbbjvLIk8esODJVxn4TnhEKqh4k'


#Database Access

cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                      ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                      'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                      'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()


analyzer = SentimentIntensityAnalyzer()
#List for storing values
vs_compound = []
holdVal = []

# Start the scheduler
sched = BackgroundScheduler()


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        try:
            tweet = all_data["text"]
            if 'RT @' not in tweet:
                filterTweet = re.sub(r"http\S+", "", tweet)
                vs = analyzer.polarity_scores(filterTweet)
                vs_compound.append(analyzer.polarity_scores(tweet)['compound'])
        except KeyError:
            'text'
        return True

    def on_error(self, status):
        print('There is an error', status)


def sent_Avg():
    sentTotal = len(vs_compound)
    avg = sum(vs_compound)/len(vs_compound)
    vs_compound.clear()
    dTime = datetime.datetime.now()
    dateS = datetime.datetime.now().date()
    dateT = datetime.datetime.now().time()
    cursor.execute("INSERT INTO dbo.sentimentValues"
                   " (sentVal,sentTotal,dateS,timeS,dateTimeS) values(?,?,?,?,?)",
                   avg,sentTotal, dateS, dateT, dTime)
    cnxn.commit()





def btc_call():
    req = requests.get('https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=0&aggregate=1&e=CCCAGG')
    open = req.json()['Data'][0]['open']
    high = req.json()['Data'][0]['high']
    low = req.json()['Data'][0]['low']
    bitVolume = req.json()['Data'][0]['volumefrom']
    dollarVol = req.json()['Data'][0]['volumeto']
    close = req.json()['Data'][0]['close']

    holdVal.insert(0, close)
    if len(holdVal) == 6:
        holdVal.pop(5)
    print(holdVal)
    if len(holdVal) >= 2:
        sma = sum(holdVal) / len(holdVal)
        deviation = stats.stdev(holdVal) * 2
        upper = sma + deviation
        lower = sma - deviation
    else:
        upper = 0
        lower = 0
    timeDate = datetime.datetime.now()
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    print('upper',upper)
    print('Lower',lower)

    cursor.execute("INSERT INTO dbo.BitcoinVal "
                   "(CLOSEPRICE, openingPrice,highPrice,lowPrice,bandUpper, bandLower ,volCoin, volEuro, dboTime,dateB,timeDate )"
                   " values(?,?,?,?,?,?,?,?,?,?,?)", close, open, high, low, upper,lower, bitVolume, dollarVol,
                   time, date, timeDate)
    cnxn.commit()




auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


sched.add_job(sent_Avg, 'interval', seconds=300)
sched.add_job(btc_call, 'interval', seconds=300)



sched.start()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Bitcoin"])
cnxn.close()



