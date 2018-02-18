import requests

# req = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
# price = req.json()['bpi']['USD']['rate']
# time = req.json()['time']['updated']
# print(price)
# print(time)
# def btc_call():
#     req = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
#     price = req.json()['bpi']['USD']['rate']
#     time = req.json()['time']['updated']
#     print(price)
#     print(time)
req = requests.get('https://api.gdax.com/btc/trades')
print(req.json())