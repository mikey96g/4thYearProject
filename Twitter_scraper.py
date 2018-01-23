import tweepy
import csv

####input your credentials here
#consumer key, consumer secret, access token, access secret.
ckey=''
csecret=''
atoken=''
asecret=''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#BitCoin
#Open/Create a file to append data
csvFile = open('letsGo.csv', 'a',newline='')
#Use csv Writer
fieldnames = ['DateTime','Tweet']
csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
csvWriter.writeheader()

for tweet in tweepy.Cursor(api.search, q="bitcoin", count=200,
                           lang="en",
                           since="2017-12-07").items():
    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        print(tweet.created_at, tweet.text)
        csvWriter.writerow({'DateTime': tweet.created_at, 'Tweet': tweet.text.encode("utf-8")})

