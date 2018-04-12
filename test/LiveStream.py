import csv
import json

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#consumer key, consumer secret, access token, access secret.
ckey='IXO7y3NtUqgZcki3KuW1p4nS0'
csecret='t1MTUtlD1TMemTqpgRyOpzKn3oMIVj3F4Rjoc4mHJsQgUahmtG'
atoken='2705490329-80t7yqBWhTvOUAZy3VC4v9SvibbabU2MMsFZuHX'
asecret='u1s6637pHzvF1aHWejgbbjvLIk8esODJVxn4TnhEKqh4k'

analyzer = SentimentIntensityAnalyzer()
class listener(StreamListener):


    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        if 'RT @' not in tweet:
            val = analyzer.polarity_scores(tweet)['compound']
            with open('stream1.csv', 'a', newline='') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(val)
                return True
        return(True)


    def on_error(self, status):
        print(status)



auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

with open('stream1.csv', 'a', newline='') as f:
    fieldnames = ['Tweet']
    csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
    csvWriter.writeheader()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Lebron"])