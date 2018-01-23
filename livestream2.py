import csv
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#consumer key, consumer secret, access token, access secret.
ckey=''
csecret=''
atoken=''
asecret=''

analyzer = SentimentIntensityAnalyzer()
vs_compound = []

class listener(StreamListener):



    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        if 'RT @' not in tweet:
            vs = analyzer.polarity_scores(tweet)
            vs_compound.append(analyzer.polarity_scores(tweet)['compound'])
            #print("{:-<65} {}".format(tweet, str(vs)))

        print("Sent Score ", vs_compound)
        return(True)


    def on_error(self, status):
        print(status)



auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)



twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bitcoin"])
