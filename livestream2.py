import json
import csv

from apscheduler.schedulers.background import BackgroundScheduler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import requests


#consumer key, consumer secret, access token, access secret.
ckey='IXO7y3NtUqgZcki3KuW1p4nS0'
csecret='t1MTUtlD1TMemTqpgRyOpzKn3oMIVj3F4Rjoc4mHJsQgUahmtG'
atoken='2705490329-80t7yqBWhTvOUAZy3VC4v9SvibbabU2MMsFZuHX'
asecret='u1s6637pHzvF1aHWejgbbjvLIk8esODJVxn4TnhEKqh4k'

analyzer = SentimentIntensityAnalyzer()
vs_compound = []

# Start the scheduler
sched = BackgroundScheduler()

class listener(StreamListener):



    def on_data(self, data):

        all_data = json.loads(data)
        try:
            tweet = all_data["text"]
            date = all_data["created_at"]
            if 'RT @' not in tweet:
                vs = analyzer.polarity_scores(tweet)
                vs_compound.append(analyzer.polarity_scores(tweet)['compound'])
                #print(analyzer.polarity_scores(tweet)['compound'])
                #print(date)
        except KeyError:
            'text'

        #print("Sent Score ",vs_compound)
        return(True)


    def on_error(self, status):
        print('There is an error', status)


def sent_Avg():

    avg = sum(vs_compound)/len(vs_compound)
    avg1 = [avg]
    vs_compound.clear()
    with open('stream3.csv', 'a', newline='') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerows(map(lambda x: [x], avg1))
    print(avg1)

def btc_call():
    req = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    price = req.json()['bpi']['USD']['rate']
    time = req.json()['time']['updated']
    print(price)
    print(time)


#def btc_15():

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

with open('stream3.csv', 'a', newline='') as f:
    fieldnames = ['Averages']
    csvWriter1 = csv.DictWriter(f, fieldnames=fieldnames)
    csvWriter1.writeheader()


sched.add_job(sent_Avg,'interval',seconds=900)
sched.add_job(btc_call, 'interval', seconds=900)
#sched.add_job(btc_call, 'interval', seconds=900)
sched.start()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Bitcoin"])

