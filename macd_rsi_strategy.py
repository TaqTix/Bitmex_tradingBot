import bitmex
import time
from bitmex_websocket import BitMEXWebsocket
import talib
from talib import MA_Type
import numpy as np
import pandas as pd

TIME_PERIOD = '1h'

def createCandles():
    TEST_EXCHANGE=True
    API_KEY="removed_for_security"
    API_SECRET="removed_for_security"

    client = bitmex.bitmex(
        test=TEST_EXCHANGE,
        api_key=API_KEY,
        api_secret=API_SECRET
    )
    ohlcv_candles = pd.DataFrame(client.Trade.Trade_getBucketed(
        binSize=TIME_PERIOD,
        symbol='XBTUSD',
        count=100,
        reverse=True
    ).result()[0])

    ohlcv_candles.set_index(['timestamp'], inplace=True)
    return ohlcv_candles
def macdStrat(candles):
    ohlcv_candles = createCandles()
    macd, signal, hist = talib.MACD(ohlcv_candles.close.values,
                                        fastperiod=8, slowperiod=28, signalperiod=9)


    print("MACD: ", hist[-2])
    print("MACD: ", hist[-1])
        # sell
    if hist[-2] > 0 and hist[-1] < 0:
        print("MACD: Sell Signal")
        return -1
    # buy
    elif hist[-2] < 0 and hist[-1] > 0:
        print("MACD: Buy Signal")
        return 1
    # do nothing
    else:
        print("MACD: Do Nothing Signal")
        return 0
def BBandStrat(candles):
    candles = createCandles()

    close = candles.close.values
    close_series = pd.Series(close) #convert ndarry to series
    
    
    upperband, middleband, lowerband = talib.BBANDS(close_series, timeperiod=60, nbdevup=2, nbdevdn=2, matype=MA_Type.SMA)
    
    upperband.fillna(0, inplace=True)
    #upperband.ffill(inplace=True)
    
    middleband.fillna(0, inplace=True)
    #middleband.ffill(inplace=True)
    
    lowerband.fillna(0, inplace=True)
    #lowerband.ffill(inplace=True)
    
    # buy
    
    non_zero_lowerband = next((index for index,value in enumerate(lowerband) if value != 0), None)
    non_zero_upperband = next((index1 for index1,value1 in enumerate(upperband) if value1 != 0), None)
    non_zero_middleband = next((index2 for index2,value2 in enumerate(middleband) if value2 != 0), None)
    # buy
    if close[0] <= lowerband[non_zero_lowerband]:
        print("BBandStrat: Buy Signal")
        return 1
    # sell (we wont want to act on this, instead we will want to ride it out)
    elif close[0] >= upperband[non_zero_upperband]:
        print("BBandStrat: Sell Signal")
        return -1
    # do nothing
    else:
        print("BBandStrat: Do Nothing Signal")
        return 0
def RSIStrat(candles):
    candles = createCandles()
    close = candles.close.values
    close_series = pd.Series(close)
    
    real = talib.RSI(close_series, timeperiod=60)
    real.fillna(0, inplace=True)
    non_zero_real = next((index for index,value in enumerate(real.to_numpy()) if value != 0), None)
    
    real_last_value = real.to_numpy()[non_zero_real]
    print("RSI: ", real_last_value)
    # buy
    if real_last_value <= 20:
        print("RSI: Buy Signal")
        return 1
    # sell
    elif real_last_value >= 80:
        print("RSI: Sell Signal")
        return -1
    else:
        print("RSI: Do Nothing Signal")
        return 0
    
    
def main():
    candles = createCandles()
    print("Close: ", candles.close.values[0])
    macdStrat(candles)
    BBandStrat(candles)
    RSIStrat(candles)
if __name__ == "__main__":
    main()
