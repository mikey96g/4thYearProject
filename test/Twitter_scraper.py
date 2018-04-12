import tweepy
import csv

####input your credentials here
consumer_key = 'IXO7y3NtUqgZcki3KuW1p4nS0'
consumer_secret = 't1MTUtlD1TMemTqpgRyOpzKn3oMIVj3F4Rjoc4mHJsQgUahmtG'
access_token = '2705490329-80t7yqBWhTvOUAZy3VC4v9SvibbabU2MMsFZuHX'
access_token_secret = 'u1s6637pHzvF1aHWejgbbjvLIk8esODJVxn4TnhEKqh4k'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#BitCoin
#Open/Create a file to append data
csvFile = open('letsGo.csv', 'a', newline='')
#Use csv Writer
fieldnames = ['DateTime', 'Tweet']
csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
csvWriter.writeheader()

for tweet in tweepy.Cursor(api.search, q="munster", count=200,
                           lang="en",
                           since="2018-01-22").items():
    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        print(tweet.created_at, tweet.text)
        csvWriter.writerow({'DateTime': tweet.created_at, 'Tweet': tweet.text.encode("utf-8")})