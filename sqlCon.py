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
csecret=''
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



