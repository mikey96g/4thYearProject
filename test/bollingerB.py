import requests
from apscheduler.schedulers.background import BackgroundScheduler

# holdVal = [] ;

# Start the scheduler

url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/latest?period_id=1MIN'
headers = {'X-CoinAPI-Key' : '73034021-0EBC-493D-8A00-E0F138111F41'}
response = requests.get(url, headers=headers)

print(response)



#holdVal = [None,None,None,None,None]

# holdVal.insert(0,2)
# holdVal.insert(0,2)
# holdVal.insert(0,2)
# holdVal.insert(0,2)
# holdVal.insert(0,3)
# holdVal.pop(4)
# holdVal.insert(0,9)
#
# print(len(holdVal))
# print(holdVal)


