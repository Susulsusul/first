import pandas as pd
import pandas_ta as ta

# csv_file_path = 'C:/Users/ASUS/Desktop/python trading/all.csv'
csv_file_path = '/root/1MinPrices.csv'

# csv_file_path =''
pure_data = pd.read_csv(csv_file_path)
pure_data = pure_data.fillna('bfill')


l1 = -20000
l2 = -1
pure_data = pd.DataFrame(pure_data[:][l1:l2])
# pure_data = pure_data.set_index(range(100))
# print(pure_data[:][-100:])

pure_data = pure_data.set_index([pd.Index(range(l2-l1))])


Currency = ["BTCUSDT", 'ETHUSDT'
            , 'XRPUSDT', 'SOLUSDT', 'TRXUSDT', 'WAVESUSDT',
            'MATICUSDT', 'LTCUSDT', 'CHZUSDT', 'BCHUSDT', 'FTMUSDT', 'DOGEUSDT', 'BNBUSDT']

Currency_BBM = pd.read_csv('/root/optimizedBBMLongV2.csv')


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

#     for  k in range(len(rsi_sellEntry)):
#         if


#     print(rsi_sellEntry)

    # crossover(vrsi, RSIoverSold)
    # vrsi = vrsi.dropna()
    # vrsi
    # rsi_buyEntry



    BBlength = 200
   #  BBmult = Currency_BBM[name]
    BBmult = Currency_BBM[name][len(Currency_BBM)-1]
    #BB std
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
#     print(BBdev)
#     BBupper = pd.DataFrame(BBupper)
#     BBupper = BBupper.apply(pd.to_numeric)
#     print(BBdev)
#     print(BBbasis)
#     print(BBbasis + BBdev)




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
    last_position = 'Short'
    fee = 0.9995
    BTC = 0
    for i in range(len(price[name])-1):

        if rsi_sellEntry[i] and sellEntry[i] and last_position !="Short":

            # print(price[name][i],df['date'][i],'Short')
            # position.append('Short')
            #
            last_position = "Short"
            total = BTC * price[name][i]


        if rsi_buyEntry[i] and buyEntry[i] and last_position !="Long":

            #  print(price[name][i],df['date'][i],'Long')

#             position.append('Long')
            last_position = "Long"
            BTC = ( total /price[name][i] ) * fee

    print("___LONG____",name,round((total-100)*10,2),"%")

#     position = []
#     total = 0
#     last_position = "Long"
#     fee = 0.9995
#     BTC = 100 / price[name][ 0 ]
#     for i in range(len(price[name])-1):
#
#
#         if rsi_sellEntry[i] and sellEntry[i] and last_position !="Short":
#
#             print(price[name][i],df['date'][i],'Short')
#             position.append('Short')
#
#             last_position = "Short"
#             total = BTC * price[name][i]
#
#
#         if rsi_buyEntry[i] and buyEntry[i] and last_position !="Long":
#
#             print(price[name][i],df['date'][i],'Long')
#
# #             position.append('Long')
#             last_position = "Long"
#             BTC = ( total /price[name][i] ) * fee
#
#    #print("___Short___",name,round(BTC * price[name][ len(price[name])-1 ],1))


