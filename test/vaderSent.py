from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import pandas as pd

vs_compound = []
df = pd.read_csv('letsGo.csv')
sentence = df.loc[:, 'Tweet']

analyzer = SentimentIntensityAnalyzer()
for sentence in sentence:
    vs = analyzer.polarity_scores(sentence)
    vs_compound.append(analyzer.polarity_scores(sentence)['compound'])
    print("{:-<65} {}".format(sentence, str(vs)))

print(vs_compound)