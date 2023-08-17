import pandas as pd
import pandas_ta as ta
import numpy as np
import csv

from telegram.ext import Updater ,CommandHandler
from telegram import Bot, BotCommand
import logging
import requests as req
from lib import CoinexPerpetualApi


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.info('Starting bot...')

access_id = '192BE1AD698D4604B9951F91FC1FD9EB'
secret_key = 'F4022AEB2BA98AD84EABED3B9C201A7CC3963862E1E2ED37'
API_KEY = '6517500629:AAHMxmiP04tDkrPS6ZuWjh5G-TdQbXswKY8'

updater = Updater(API_KEY)
bot = Bot(API_KEY)
robot = CoinexPerpetualApi(access_id, secret_key)



dp = updater.dispatcher







# csv_file_path = 'C:/Users/ASUS/Desktop/python trading/all.csv'
csv_file_path = '/root/1MinPrices.csv'

pure_data = pd.read_csv(csv_file_path)
pure_data = pure_data.fillna('bfill')


Currency = ["BTCUSDT", 'ETHUSDT'
         , 'XRPUSDT', 'SOLUSDT', 'TRXUSDT', 'WAVESUSDT',
         'MATICUSDT', 'LTCUSDT', 'CHZUSDT', 'BCHUSDT', 'FTMUSDT', 'DOGEUSDT', 'BNBUSDT']


Currency_BBM = pd.read_csv('/root/testp.csv')

last_position =  pd.read_csv('/root/Lastposition.csv')
Complete_opti = []
last_position_append = []
for name in Currency:
    opti = []

    df = pd.DataFrame(pure_data[['date',name]])

    price = pd.DataFrame(df[name])
    price = price.apply(pd.to_numeric)
    # len(df)
    date = pd.DataFrame(df['date'])

    RSIlength = 6  #"RSI Period Length")
    RSIoverSold = 50
    RSIoverBought = 50
    vrsi = ta.rsi(price[name], RSIlength)
#     print(vrsi)

    rsi_buyEntry = vrsi < RSIoverSold
    rsi_sellEntry= vrsi > RSIoverBought




    BBlength = 200
#     BBmult = Currency_BBM[name] #BB std
    BBmult = Currency_BBM[name][len(Currency_BBM)-1]
#     print(name,BBmult)
    BBbasis = ta.sma(price[name])
#   print(BBbasis)
    BBbasis = pd.DataFrame(BBbasis)
    BBbasis = BBbasis.apply(pd.to_numeric)
    BBbasis = BBbasis.fillna(method='bfill')

    stdev = ta.stdev(price[name], BBlength)
    stdev = pd.DataFrame(stdev)
    stdev = stdev.apply(pd.to_numeric)
    stdev = stdev.fillna(method='bfill')

#    print(stdev)
    BBdev = BBmult * stdev
    BBdev = pd.DataFrame(BBdev)
    BBdev = BBdev.apply(pd.to_numeric)

    BBupper = BBbasis['SMA_10']+BBdev['STDEV_200']





    BBlower = BBbasis['SMA_10']-BBdev['STDEV_200']


    buyEntry = price[name] < BBlower
    sellEntry = price[name] > BBupper






#    now_price = price[name][len(price)-1]
#    Amount = 20 / now_price

#   bot.send_message(75842418, f'{name}:{Amount}')
#   bot.send_message(75842418, rsi_sellEntry[10])
   #bot.send_message(75842418, last_position[name][len(last_position)-1])
   # bot.send_message(75842418, sellEntry[len(sellEntry)-1])
  # bot.send_message(75842418, price[name][len(price)-1])
#     print(len(price[name])-1)
    position = []
    total = 100
    fee = 0.9995
    BTC = 0
    # for i in range(len(price[name])-1):

    short_pos = False
    if rsi_sellEntry[len(rsi_sellEntry)-1] and sellEntry[len(sellEntry)-1] and last_position[name][len(last_position)-1] !="Short":

        # position.append('Short')
        last_position_append.append("Short")
        # total = BTC * price[name][i]
        text_Short = f'#LONGBOT\n🔴Short #{name}\nPrice : {price[name][len(price)-1]}\n#danger'
        bot.send_message(75842418, text_Short)
        bot.send_message(6001006306, text_Short)
        short_pos = True
        try:
            q = robot.query_position_pending(name)
            pos_id = q['data'][0]["position_id"]
            bot.send_message(75842418,f'Position ID : {pos_id}')
            c = robot.close_market(name, pos_id)
        except:
            bot.send_message(75842418, f'❌❌Failed to Close Position!!❌❌\n{name}:{price[name][len(price) - 1]}')
            bot.send_message(6001006306, f'❌❌Failed to Close Position!!❌❌\n{name}:{price[name][len(price) - 1]}')

    if rsi_buyEntry[len(rsi_buyEntry)-1] and buyEntry[len(buyEntry)-1] and last_position[name][len(last_position)-1] !="Long":

        now_price = price[name][len(price)-1]
        Amount = 16 / now_price

        last_position_append.append("Long")
        text_Long = f'#LONGBOT\n🟢Long #{name}\nPrice : {price[name][len(price)-1]}\n#danger'
        bot.send_message(75842418, text_Long)
        bot.send_message(6001006306, text_Long)
        try:
            #print(1)
#_________________________________________________
            response_Levrage = robot.adjust_leverage(market=name, position_type=1, leverage=10)
            bot.send_message(75842418, response_Levrage)

            response_market = robot.put_market_order(market=name, side=2, amount=Amount)
            bot.send_message(75842418, response_market)
            bot.send_message(6001006306, f'Opend {name}')
            bot.send_message(75842418, f'Opend {name}')
        except:
            bot.send_message(75842418, f'❌❌Failed to trade!!❌❌\n{name}:{price[name][len(price)-1]}')
            bot.send_message(6001006306, f'❌❌Failed to trade!!❌❌\n{name}:{price[name][len(price)-1]}')



    else :

        if short_pos!=True:
            # bot.send_message(75842418,'No signal Bitch!!')
            last_position_append.append(last_position[name][len(last_position)-1])
print(last_position_append)
with open('/root/Lastposition.csv', 'a', newline='') as csv_file:

    writerObj = csv.writer(csv_file)
    writerObj.writerow(last_position_append)
            # BTC = ( total /price[name][i] ) * fee




# print(Complete_opti)
# with open('optimize.csv', 'a', newline='') as csv_file:
#
#     writerObj = csv.writer(csv_file)
#     writerObj.writerow(Complete_opti)

