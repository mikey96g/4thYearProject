from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer
import csv
import pandas as pd
import datetime as d

# --- examples -------
#sentences = ["VADER is smart, handsome, and funny.",      # positive sentence example
            # "VADER is not smart, handsome, nor funny.",   # negation sentence example
            # "VADER is smart, handsome, and funny!",       # punctuation emphasis handled correctly (sentiment intensity adjusted)
            # "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
            # "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
            # "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
            # "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",# booster words & punctuation make this close to ceiling for score
            # "The book was good.",                                     # positive sentence
            # "The book was kind of good.",                 # qualified positive sentence is handled correctly (intensity adjusted)
            # "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
            # "At least it isn't a horrible book.",         # negated negative sentence with contraction
            # "Make sure you :) or :D today!",              # emoticons handled
            # "Today SUX!",                                 # negative slang with capitalization emphasis
            # "Today only kinda sux! But I'll get by, lol"  # mixed sentiment example with slang and constrastive conjunction "but"
            #  ]

# with open('new.csv', 'r') as input:
#     reader = csv.reader(input)
#     for row in reader:
#         print(row)
# vs_compound = []
df = pd.read_csv('letsGo1.csv')
sentence = df.loc[:,'DateTime']
print(df.dtypes)

df['DateTime'] = pd.to_datetime(df['DateTime'])
print(df.dtypes)

for i in sentence:
    df['Time'], df['Date'] = df['DateTime'].apply(lambda x: x.time()), df['DateTime'].apply(lambda x: x.date())
print(df)










# sentence = df.loc[:,'Tweet']
#
# analyzer = SentimentIntensityAnalyzer()
# for sentence in sentence:
#     vs = analyzer.polarity_scores(sentence)
#     vs_compound.append(analyzer.polarity_scores(sentence)['compound'])
#     print("{:-<65} {}".format(sentence, str(vs)))
#
# print(vs_compound)
# df['new_timeStamp'] = pd.to_datetime(df.DateTime)

#print(df.DateTime.iat[0])
# df['new_date'] = [d.date() for c in df['DateTime']]
#
# df['new_time'] = [d.time() for c in df['DateTime']]
# print(pd.to_datetime(df.DateTime.iat[0]))
# pd.to_datetime(df.DateTime)


#bad_data = []
#for n, ts in enumerate(df.DateTime):
#    try:
#        print(pd.to_datetime(ts))
#
 #   except:
#
 #       bad_data.append(n, ts)













