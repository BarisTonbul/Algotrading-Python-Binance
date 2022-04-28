import json,config,math,requests,time
from binance.client import Client
from binance.enums import *
import threading
import time
from datetime import datetime
import time
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import numpy as np
import pandas_ta as pta



# Indicator Client
client = Client(config.API_KEY, config.API_SECRET)

# Variables
openPositions = {}

# Functions
def getPrecision(Ticker):
    while(True):
        try:
            info = client.futures_exchange_info()
            requestedFutures = [Ticker]
            ListOfPrecisions = {si['symbol']:si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures}
            return ListOfPrecisions.get(Ticker)
        except Exception as e :
            print(f"{Ticker} getPrecision couldnt get")
            time.sleep(1)
def ChangeLeverage(Symbol,Leverage):
    x = 0
    while(x < 3):
        try:
            client.futures_change_leverage(symbol=Symbol,leverage=Leverage,maxNotionalValue="1000000")
            break
        except Exception as e:
            print(f"{Symbol} change levereage error ! {e}")
            time.sleep(1)
            x = x + 1
def changeMarginType(Symbol):
    x = 0
    while(x < 3):
        try:
            client.futures_change_margin_type(symbol=Symbol,marginType="ISOLATED")
            break
        except Exception as e : 
            print(f"{Symbol} marginType error ! {e}")
            time.sleep(1)
            x = x + 1
def getCurrentPrice(Symbol):
    while(True):
        try:
            price = client.futures_symbol_ticker(symbol=Symbol)
            price = float(price.get("price"))
            return price
        except Exception as e :
            print(f"{Symbol} currentPrice couldnt get ! {e}")
            time.sleep(1)
def openLong(Symbol,Quantity):
    while(True):
        try:
            client.futures_create_order(symbol=Symbol, side="BUY", type="MARKET",quantity=Quantity,positionSide="LONG")
            break
        except Exception as e :
            print(f"{Symbol} open market long error ! {e}")
            time.sleep(1)
def closeLong(Ticker,precision):
    try:
        quantity = round(getPositionQuantityLong(Ticker),precision)
        client.futures_create_order(symbol=Ticker,side="SELL",type='MARKET',quantity=quantity,positionSide="LONG")
    except Exception as e :
        print(f"{Ticker} closeLong error", e)
        time.sleep(1)
def getPositionQuantityLong(Ticker):
    try:
        orders = client.futures_position_information(symbol=Ticker)
        order = orders[1]
        quantity = order.get("positionAmt")
        quantity = float(quantity)
        return quantity
    except Exception as e :
        print(f"{Ticker} positionQty couldnt get x:{x}")
        time.sleep(1)
def openShort(Ticker,quantity):
    while(True):
        try:
            # ChangeLeverage("BTCUSDT", 50)
            client.futures_create_order(symbol=Ticker,side="SELL",type="MARKET",quantity=quantity,positionSide="SHORT")
            break
        except Exception as e :
            print(f"{Ticker} open SHORT error {e}")
            time.sleep(1)
def closeShort(Ticker,precision):
    try:
        quantity = round(getPositionQuantityShort(Ticker),precision)
        client.futures_create_order(symbol=Ticker,side="BUY",type='MARKET',quantity=quantity,positionSide="SHORT")
    except Exception as e :
        print(f"{Ticker} close SHORT error")
        time.sleep(1)
def getPositionQuantityShort(Ticker):
    try:
        orders = client.futures_position_information(symbol=Ticker)
        order = orders[::-1][0]
        quantity = order.get("positionAmt")
        quantity = float(quantity[1:])
        return quantity
    except Exception as e :
        print(f"{Ticker} positionQty couldnt get e:{e}")
        time.sleep(1)
def computeRSI(data, time_window):
    diff = np.diff(data)
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    up_chg = pd.DataFrame(up_chg)
    down_chg = pd.DataFrame(down_chg)
    
    up_chg_avg   = up_chg.ewm(com=time_window , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    rsi = int(rsi[0].iloc[-1])
    return rsi
def getRSIValue(Ticker):
    while(True):
        try:
            klines = client.futures_klines(symbol=Ticker, interval='15m', limit='200')
            close = [float(entry[4]) for entry in klines]
            close_array = np.asarray(close)
            rsiValue = computeRSI(close_array,12)
            break
        except:
            pass
    return rsiValue


# ---------------------------------

# Long Position Opener
def longPosition(Ticker,precision,leverage,x1Dollar,x2Dollar,rsi1,rsi2):
    print(f"{Ticker} LONG bakilmaya baslandi")
    ChangeLeverage(Ticker,leverage) # Change leverage
    changeMarginType(Ticker)  # Change margin type to ISOLATED

    openPositions[f"{Ticker}"] = 0 # Bot started following rsi value // Phase 0
    check = True

    while(check): # Checking starting

        currentPrice = getCurrentPrice(Ticker)
        rsiValue = getRSIValue(Ticker)
        print(f"{Ticker} rsiValue:{rsiValue}")

        if((rsiValue < rsi1) & (openPositions.get(f"{Ticker}")== 0) ):
            # Open Long Position for x1 money
            quantity = round((x1Dollar/currentPrice*leverage),precision) 
            openLong(Ticker,quantity)
            # Set dictionary
            openPositions[f"{Ticker}"] = 1 # First position opened // Phase 1
            print(f"{Ticker} first position opened. ")
        elif((rsiValue < rsi2) & (openPositions.get(f"{Ticker}")== 1)):
            # Open Long Position for x2 money
            quantity = round((x2Dollar/currentPrice*leverage),precision) 
            openLong(Ticker,quantity)
            # Set dictionary
            openPositions[f"{Ticker}"] = 2 # Second position opened // Phase 2
            print(f"{Ticker} Second position opened. ")
        elif(rsiValue > 30):  # Sell order, take profit or stop loss
            x = 1
            while(True):
                # Close position
                if(x < 5):
                    try:
                        x = x + 1
                        closeLong(Ticker,precision) # Closing position with market sell // Maximum 5 tries
                        check = False
                        break
                    except:
                        print(f"{Ticker} Close LONG position error")
                else:
                    check = False
                    break
            # Set dictionary 
            openPositions.pop(f"{Ticker}") # Remove from followings list
            check=False
            print(f"{Ticker} LONG position has been closed.")    


# Short Position Opener
def shortPosition(Ticker,precision,leverage,x1Dollar,x2Dollar,rsi1,rsi2):
    print(f"{Ticker} SHORT bakilmaya baslandi")
    ChangeLeverage(Ticker,leverage) # Change leverage
    changeMarginType(Ticker)  # Change margin type to ISOLATED

    openPositions[f"{Ticker}"] = 0 # Bot started following rsi value // Phase 0
    check = True

    while(check): # Checking starting
        currentPrice = getCurrentPrice(Ticker)
        rsiValue = getRSIValue(Ticker)
        print(f"{Ticker} rsiValue:{rsiValue}")
        if((rsiValue > rsi1) & (openPositions.get(f"{Ticker}")== 0) ):
            # Open Short Position for x1 money
            quantity = round((x1Dollar/currentPrice*leverage),precision) 
            openShort(Ticker,quantity)
            # Set dictionary
            openPositions[f"{Ticker}"] = 1 # First position opened // Phase 1
            print(f"{Ticker} first position opened. ")
        elif((rsiValue > rsi2) & (openPositions.get(f"{Ticker}")== 1)):
            # Open Short Position for x2 money
            quantity = round((x2Dollar/currentPrice*leverage),precision) 
            openShort(Ticker,quantity)
            # Set dictionary
            openPositions[f"{Ticker}"] = 2 # Second position opened // Phase 2
            print(f"{Ticker} Second position opened. ")
        elif(rsiValue < 90):  # Sell order, take profit or stop loss
            x = 1
            while(True):
                # Close position
                if(x < 5):
                    try:
                        x = x + 1
                        closeShort(Ticker,precision) # Closing position with market Buy // Maximum 5 tries
                        check = False
                        break
                    except:
                        print(f"{Ticker} Close Short position error")
                else:
                    check = False
                    break
            # Set dictionary 
            openPositions.pop(f"{Ticker}") # Remove from followings list
            check=False
            print(f"{Ticker} Short position has been closed.")    

