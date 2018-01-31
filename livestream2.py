import json
import csv

from apscheduler.schedulers.blocking import BlockingScheduler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#consumer key, consumer secret, access token, access secret.
ckey='IXO7y3NtUqgZcki3KuW1p4nS0'
csecret='t1MTUtlD1TMemTqpgRyOpzKn3oMIVj3F4Rjoc4mHJsQgUahmtG'
atoken='2705490329-80t7yqBWhTvOUAZy3VC4v9SvibbabU2MMsFZuHX'
asecret='u1s6637pHzvF1aHWejgbbjvLIk8esODJVxn4TnhEKqh4k'

analyzer = SentimentIntensityAnalyzer()
vs_compound = []

class listener(StreamListener):



    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        date = all_data["created_at"]
        if 'RT @' not in tweet:
            vs = analyzer.polarity_scores(tweet)
            vs_compound.append(analyzer.polarity_scores(tweet)['compound'])
            print(analyzer.polarity_scores(tweet)['compound'])
            print(date)


        print("Sent Score ",vs_compound)
        return(True)


    def on_error(self, status):
        print(status)

    # def sent_Avg():
    #     print("")


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)



twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Lou"])
