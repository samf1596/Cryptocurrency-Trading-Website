from datetime import datetime, timedelta
import time
import threading
import json
import requests
import sys

from home.models import Old_Prices, Coins


def StoreData():
    pass


def DataStream():
    while True:
        # set the time to stream the data
        timeToRun = datetime.now() + timedelta(seconds=10)

        # Request data from coinmarketcap and parse the data
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/')
        for coin in r.json():

            print(datetime.now(), coin["symbol"], coin["price_usd"], )
            if not Coins.objects.filter(ticker=coin["symbol"]).exists():
                coinz = Coins(ticker=coin["symbol"], website="http", current_price=coin["price_usd"], gain_loss=0)
                coinz.save()
            else:
                coinz = Coins.objects.get(ticker=coin["symbol"])

            Price = Old_Prices(timestamp=datetime.now(), ticker=coinz, accuracy_projection=0, price=coin["price_usd"])
            Price.save()

        # Wait until timeToRun has passed to fetch new data
        while datetime.now() < timeToRun:
            time.sleep(1)


t1 = threading.Thread(target=DataStream)


def StartStream():
    # Create a thread to run the data stream
    t1.start()


StartStream()
