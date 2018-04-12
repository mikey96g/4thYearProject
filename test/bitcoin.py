import requests
import json
price=[5]

req = requests.get('https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=0&aggregate=1&e=CCCAGG')
price = req.json()['Data'][0]
print(price)

#####
close = req.json()['Data'][0]['close']
print(close)

#####
high = req.json()['Data'][0]['high']
print(high)

#####
low = req.json()['Data'][0]['low']
print(low)

#####
open = req.json()['Data'][0]['open']
print(open)

#####
bitVolume = req.json()['Data'][0]['volumefrom']
print(bitVolume)

#####
dollarVol = req.json()['Data'][0]['volumeto']
print(dollarVol)