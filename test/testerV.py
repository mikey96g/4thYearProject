# import pandas as pd
# import datetime
# df = pd.read_csv('letsGo1.csv')
# sentence = df.loc[:,'DateTime']
# print(df.dtypes)
#
# df['DateTime'] = pd.to_datetime(df['DateTime'])
# print(df.dtypes)
#
# for i in sentence:
#     df['Time'], df['Date'] = df['DateTime'].apply(lambda x: x.time()), df['DateTime'].apply(lambda x: x.date())
# print(df)
#
# time = df.loc[:,'Time']
# for b in time:
#     if  < 24:
#         print(time)
# print(df.head())
# for  i in sentence:
#     if ()



# totalScore = sum(vs_compound)
        # count = len(vs_compound)
        # avgSent = totalScore/count
        # print("Sent Score ", totalScore, " ----- ", avgSent, " ----- ",count," ----- ", vs_compound)

# b("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+://\S+)", " ", tweet).split())#Utility function to clean tweet text by removing links, special characters
# using simple regex statements.
# '''
# return ' '.join(re.su