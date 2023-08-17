import pandas as pd
import pandas_ta as ta
from time import sleep

from telegram.ext import Updater ,CommandHandler
from telegram import Bot, BotCommand
API_KEY = '6517500629:AAHMxmiP04tDkrPS6ZuWjh5G-TdQbXswKY8'
updater = Updater(API_KEY)
#dp = updater.dispatcher


bot = Bot(API_KEY)

csv_file_path = '/root/5MinPrices.csv'

pure_data = pd.read_csv(csv_file_path)
pure_data = pure_data.fillna('bfill')


# l1 = -23000
# l2 = -1
# pure_data = pd.DataFrame(pure_data[:][l1:l2])
# print(pure_data[:][-100:])
# pure_data = pure_data.set_index([pd.Index(range(l2-l1))])


Currency = ["BTCUSDT", 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'TRXUSDT',
            'WAVESUSDT','MATICUSDT', 'LTCUSDT', 'CHZUSDT', 'BCHUSDT',
            'FTMUSDT', 'DOGEUSDT', 'BNBUSDT', 'NEARUSDT', 'GMTUSDT',
            'DASHUSDT','AVAXUSDT']

#Currency_BBM = pd.read_csv('/root/optimizedBBMLongV2.csv')
Currency_BBM = pd.read_csv('/root/optimizedBBMLong5minV0.csv')

#Currency_BBM = {
#"BTCUSDT":1.7 ,
#'ETHUSDT' :2.2 ,
#'XRPUSDT' :2.0 ,
#'SOLUSDT' :1.8 ,
#'TRXUSDT' :2.4 ,
#'WAVESUSDT': 2.4 ,
#'MATICUSDT' :1.5 ,
#'LTCUSDT': 2.2 ,
#'CHZUSDT' :2.3 ,
#'BCHUSDT' :2.8 ,
#'FTMUSDT': 1.9 ,
#'DOGEUSDT' :1.8 ,
#'BNBUSDT' :1.6}


for name in Currency:

    #bot.send_message(75842418, name)
    #bot.send_message(6001006306,name)

    df = pd.DataFrame(pure_data[['date',name]])

    price = pd.DataFrame(df[name])
    price = price.apply(pd.to_numeric)
    date = pd.DataFrame(df['date'])



    RSIlength = 6  #"RSI Period Length")
    RSIoverSold = 50
    RSIoverBought = 50
    vrsi = ta.rsi(price[name], RSIlength)

    rsi_buyEntry = vrsi < RSIoverSold
    rsi_sellEntry= vrsi > RSIoverBought



    BBlength = 200
    BBmult = Currency_BBM[name][len(Currency_BBM)-1]
    BBbasis = ta.sma(price[name])
    BBbasis = pd.DataFrame(BBbasis)
    BBbasis = BBbasis.apply(pd.to_numeric)
    BBbasis = BBbasis.fillna(method='bfill')

    stdev = ta.stdev(price[name], BBlength)
    stdev = pd.DataFrame(stdev)
    stdev = stdev.apply(pd.to_numeric)
    stdev = stdev.fillna(method='bfill')


    BBdev = BBmult * stdev
    BBdev = pd.DataFrame(BBdev)
    BBdev = BBdev.apply(pd.to_numeric)

    BBupper = BBbasis['SMA_10']+BBdev['STDEV_200']




    BBlower = BBbasis['SMA_10']-BBdev['STDEV_200']
#     BBlower = pd.DataFrame(BBlower)
#     BBlower = BBlower.apply(pd.to_numeric)

    buyEntry = price[name] < BBlower
    sellEntry = price[name] > BBupper

#     print(BBlower)
    # ta.bbands(df['close'])






#     print(len(price[name])-1)
#     position = []
    initial_amount = 30
    # total = 30
    last_position = 'Short'
    fee = 0.9995
    # BTC = 0
    pft_t = 0
    trade_count = 0
    profit_count = 0
    loss_count = 0
    
    for i in range(len(price[name])-1):
    
        if rsi_sellEntry[i] and sellEntry[i] and last_position !="Short":

            pft =(price[name][i]-last_price)/last_price * initial_amount *fee
            pft_t += round(pft,4)
            tt = f'\nPROFIT : {round(pft,4)} $'
            #sleep(0.1)

           # print(tt)
           # print(last_date,date.iloc[i],sep='\n')
           # print('BuyPrice : ',last_price,'\nSellPrice : ',price[name][i])

            #bot.send_message(75842418, tt)
            #bot.send_message(6001006306, tt)
            
            # total = BTC * price[name][i]
            nowprice=price[name][i]
            now_date = date["date"][i]
            if nowprice>last_price:
                profit_count+=1
            else:
                loss_count+=1
            last_position = "Short"
            trade_count+=1
            tsttxt_s = f'{date["date"][i]} _S_ {nowprice}'

            print(tsttxt_s)
            #print((nowprice-last_price)/last_price * initial_amount,"\n")
            tstamin = f"#{name}\nopen date:{last_date}\nclose date:{now_date}\nopen price:{last_price}\nclose price:{nowprice}"
           

    #_________________________trade list data
           # if name =='DOGEUSDT' or name=='FTMUSDT' or name=='WAVESUSDT' or name=='LTCUSDT' or name=='XRPUSDT' or name=='TRXUSDT':
                #sleep(0.2)
                #bot.send_message(75842418, tstamin)
                #bot.send_message(6001006306,tstamin)

        try:
            if rsi_buyEntry[i] and buyEntry[i] and last_position !="Long":

                last_position = "Long"
                # BTC = ( total /price[name][i] ) * fee
                last_price = price[name][i]
                last_date = date["date"][i]
                tsttxt = f'{last_date} _L_ {last_price}'
                print(tsttxt)
            status = {'name':name,
                    'profit':round(pft_t,4),
                    'win':profit_count,
                    'lose':loss_count
                        }
        except:
            bot.send_message(75842418, 'Long signal something wrong!!')
    # text =f"❌ Wronge Profit {name} : {round((total-initial_amount)*10,4)} $"
    pft_text = f'✅ Real Profit {name} : {round(pft_t,4)} $ _ TradeCounts : {trade_count}'
    print(pft_text)
    #print(f'profit Count : {profit_count} , Loss Count : {loss_count}\n')
    print(status)
   
    #sleep(0.5)
    #print(tex)
    #bot.send_message(75842418, pft_text)
    #bot.send_message(6001006306, pft_text)
    #bot.send_message(75842418, text)
    #bot.send_message(6001006306,text)


