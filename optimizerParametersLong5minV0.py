import pandas as pd
import pandas_ta as ta
import numpy as np
import csv

csv_file_path = '/root/5MinPrices.csv'
pure_data = pd.read_csv(csv_file_path)
pure_data = pure_data.fillna('bfill')

# l1 = -23000
# l2 = -1
# pure_data = pd.DataFrame(pure_data[:][l1:l2])
# print(pure_data[:][-100:])
# pure_data = pure_data.set_index([pd.Index(range(l2-l1))])),    pure_data  )


Currency = ["BTCUSDT", 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'TRXUSDT',
            'WAVESUSDT','MATICUSDT', 'LTCUSDT', 'CHZUSDT', 'BCHUSDT',
            'FTMUSDT', 'DOGEUSDT', 'BNBUSDT', 'NEARUSDT', 'GMTUSDT',
            'DASHUSDT','AVAXUSDT']


Complete_opti = []
for name in Currency:
    opti = []

    for ll in np.arange(0.7,5.0,0.1):
#     for name in Currency:



        df = pd.DataFrame(pure_data[['date',name]])

        price = pd.DataFrame(df[name])
        price = price.apply(pd.to_numeric)
        # len(df)
        # df




        RSIlength = 6  #"RSI Period Length")
        RSIoverSold = 50
        RSIoverBought = 50
        vrsi = ta.rsi(price[name], RSIlength)
    #     vrsi = pd.DataFrame(vrsi)
    #     vrsi = vrsi.apply(pd.to_numeric)
    #     vrsi = vrsi.fillna(method='bfill')
    #     print(vrsi)

        rsi_buyEntry = vrsi < RSIoverSold
        rsi_sellEntry= vrsi > RSIoverBought



        BBlength = 200
    #     BBmult = Currency_BBM[name] #BB std
        BBmult=ll
    #     print(name,BBmult)
        BBbasis = ta.sma(price[name])
    #     print(BBbasis)
        BBbasis = pd.DataFrame(BBbasis)
        BBbasis = BBbasis.apply(pd.to_numeric)
        BBbasis = BBbasis.fillna(method='bfill')

        stdev = ta.stdev(price[name], BBlength)
        stdev = pd.DataFrame(stdev)
        stdev = stdev.apply(pd.to_numeric)
        stdev = stdev.fillna(method='bfill')

    #     print(stdev)
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
        position = []
        total = 100
        last_position = None
        fee = 0.9995
        BTC = 0
        for i in range(len(price[name])-1):


            if rsi_sellEntry[i] and sellEntry[i] and last_position !="Short":

                position.append('Short')
                last_position = "Short"
                total = BTC * price[name][i] * fee


            if rsi_buyEntry[i] and buyEntry[i] and last_position !="Long":

                last_position = "Long"
                BTC = ( total /price[name][i] ) * fee
        
        
        opti.append(round(ll,2))
        opti.append(round(total,2))
    
    if opti[opti.index(max(opti))-1] == 0.0 or opti[opti.index(max(opti))]<=101:
        Complete_opti.append(1000)


    else:
        Complete_opti.append( opti[opti.index(max(opti))-1] )
    print(name,opti[opti.index(max(opti))-1],opti[opti.index(max(opti))])
    #print(name,opti)

        # print("___LONG____",f'BBM={round(ll,1)}',name,round(total,2))



print(Complete_opti)
with open('optimizedBBMLong5minV0.csv', 'a',newline='') as csv_file:
 
    writerObj = csv.writer(csv_file)
    writerObj.writerow(Complete_opti)


