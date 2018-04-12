import json
import csv
import statistics as st


from apscheduler.schedulers.background import BackgroundScheduler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import requests
import re

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
            if 'RT @' not in tweet:
                print(tweet)
                filterTweet = re.sub(r"http\S+", "", tweet)
                print(filterTweet)
                vs = analyzer.polarity_scores(filterTweet)
                vs_compound.append(analyzer.polarity_scores(tweet)['compound'])
        except KeyError:
            'text'
        return True

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

# def btc_call():
#     req = requests.get(
#         'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=0&aggregate=1&e=CCCAGG')
#     close = req.json()['Data'][0]['close']
#     open = req.json()['Data'][0]['open']
#     high = req.json()['Data'][0]['high']
#     low = req.json()['Data'][0]['low']
#     bitVolume = req.json()['Data'][0]['volumefrom']
#     dollarVol = req.json()['Data'][0]['volumeto']
#     holdVal = []
#     holdVal.insert(0, close)
#     sma = sum(holdVal) / len(holdVal)
#     if len(holdVal) == 6:
#         holdVal.pop(5)
#     if len(holdVal) >= 2:
#         deviation = st.stdev(holdVal) * 2
#         upper = sma + deviation
#         lower = sma - deviation
#         print("Upper:", upper)
#         print("Lower:", lower)
#         print("Deviation:", deviation)
    
    # print("Open:", open)
    # print("Close:", close)
    # print("High:", high)
    # print("Low:", low)
    # print("BitcoinVolume:", bitVolume)
    # print("dollarVolume:", dollarVol)//  print("sma")




# def bollinger_band():
#     req = requests.get('https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=0&aggregate=1&e=CCCAGG')
#     close = req.json()['Data'][0]['close']
#     holdVal = []
#     holdVal.insert(0,close)
#     if len(holdVal) == 6:
#         holdVal.pop(5)
#     sma = sum(holdVal)/len(holdVal)
#     deviation = np.std(holdVal)*2
#     upper = sma + deviation
#     lower = sma - deviation
#     print("Deviation",deviation)
#     print(upper)
#     print(lower)





#def btc_15():

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

with open('stream3.csv', 'a', newline='') as f:
    fieldnames = ['Averages']
    csvWriter1 = csv.DictWriter(f, fieldnames=fieldnames)
    csvWriter1.writeheader()


sched.add_job(sent_Avg,'interval',seconds=60)
#sched.add_job(btc_call, 'interval', seconds=60)
# sched.add_job(bollinger_band, 'interval', seconds=60)
#sched.add_job(btc_call, 'interval', seconds=900)
sched.start()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Bitcoin"])
