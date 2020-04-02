# Bitmex_tradingBot

So far bot fetches data from bitmex API regarding previous closing values on the 1m charts.  It then constructs ovch candles & uses a
C-wrapper TA-Lib to perform Technical Analysis logic.

Implemented features (logic follows investopedia):

MacD Strategy  RSI Strategy 


Example Usage (already provided in script):


'def main():
    candles = createCandles()
    print("Close: ", candles.close.values[0])
    macdStrat(candles)
    BBandStrat(candles)
    RSIStrat(candles)
if __name__ == "__main__":
    main()'
    
    
    
