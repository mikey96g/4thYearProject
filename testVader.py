from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import pandas as pd



df = pd.read_csv('letsGo.csv')
sentence = df.loc[:,'Tweet']

#Open/Create a file to append data
csvFile = open('new.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

analyzer = SentimentIntensityAnalyzer()
for sentence in sentence:
    vs = analyzer.polarity_scores(sentence)

    print("{:-<65} {}".format(sentence, str(vs)))
	csvWriter.writerow(["{:-<65} {}".format(sentence, str(vs))])













