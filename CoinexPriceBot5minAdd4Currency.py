import requests as req
import pytz
from datetime import datetime
import csv

Market_Status_URL = 'https://api.coinex.com/perpetual/v1/market/ticker/all'

Currency = ["BTCUSDT", 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'TRXUSDT', 'WAVESUSDT',
            'MATICUSDT', 'LTCUSDT', 'CHZUSDT','BCHUSDT', 'FTMUSDT', 'DOGEUSDT',
            'BNBUSDT','NEARUSDT','GMTUSDT','DASHUSDT','AVAXUSDT']# , 'NEARUSDT','GMTUSDT','DASHUSDT','AVAXUSDT']

with open('5MinPrices.csv', 'a', newline='') as csv_file:

    writerObj = csv.writer(csv_file)




    time_irani = datetime.now(pytz.timezone('Asia/Tehran'))
    Now_date = str(time_irani)[:16]

    now_price = req.get(Market_Status_URL)
    price_list = [Now_date]


    for i in Currency:
        Currency_Price = now_price.json()['data']['ticker'][i]['last']
        price_list.append( Currency_Price )


    writerObj.writerow(price_list)


