import json,math,requests,time,threading,time
from binance.client import Client
# from binance.enums import *
from flask import Flask, request, jsonify,render_template
import logging
from datetime import datetime
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import numpy as np
import pandas_ta as pta

# Flask app name
app = Flask(__name__)

API1 = "" # Key
API2 = "" # Secret Key

# Client
client = Client(API1, API2)

# Precision
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
# Change Leverage
def ChangeLeverage(Ticker,Leverage):
    x = 0
    while(x < 3):
        try:
            client.futures_change_leverage(symbol=Ticker,leverage=Leverage,maxNotionalValue="1000000")
            break
        except Exception as e:
            print(f"{Ticker} change levereage error ! {e}")
            time.sleep(1)
            x = x + 1
# Margin Type
def changeMarginType(Ticker,stringMargin): # ISOLATED & CROSSED
    x = 0
    while(x < 3):
        try:
            client.futures_change_margin_type(symbol=Ticker,marginType=stringMargin)
            break
        except Exception as e : 
            print(f"{Ticker} marginType error ! {e}")
            time.sleep(1)
            x = x + 1
# Current Price
def getCurrentPrice(Ticker):
    while(True):
        try:
            price = client.futures_symbol_ticker(symbol=Ticker)
            price = float(price.get("price"))
            return price
        except Exception as e :
            print(f"{Ticker} currentPrice couldnt get ! {e}")
            time.sleep(1)            
# Long Market Open
def openMarketLong(Ticker,Quantity):
    while(True):
        try:
            order = client.futures_create_order(symbol=Ticker, side="BUY", type="MARKET",quantity=Quantity,positionSide="LONG")
            return order["orderId"]
        except Exception as e :
            print(f"{Ticker} open market long error ! {e}")
            time.sleep(1)
# Long Position Quantity
def getPositionQuantityLong(Ticker):
    while(True):
        try:
            orders = client.futures_position_information(symbol=Ticker)
            order = orders[1]
            quantity = order.get("positionAmt")
            quantity= float(quantity)
            return quantity
        except Exception as e:
            print(f"{Ticker} get quantity error ! {e}")
            time.sleep(1)
# Long Market Close
def closeMarketLong(Ticker,precision):
    while(True):
        try:
            quantity = round(getPositionQuantityLong(Ticker),precision)
            client.futures_create_order(symbol=Ticker, side="SELL", type="MARKET", quantity=quantity, positionSide="LONG")
            break
        except Exception as e :
            print(f"{Ticker} closeLong error ! {e}")
            time.sleep(1)
# Short Market Open
def openMarketShort(Ticker,Quantity):
    while(True):
        try:
            order = client.futures_create_order(symbol=Ticker, side="SELL", type="MARKET", quantity=Quantity, positionSide="SHoRT")
            return order["orderId"]
        except Exception as e:
            print(f"{Ticker} open market short error ! {e}")
            time.sleep(1)
# Short Position Quantity
def getPositionQuantityShort(Ticker):
    while(True):
        try:
            orders = client.futures_position_information(symbol=Ticker)
            order = orders[::-1][0]
            quantity = order.get("positionAmt")
            quantity = float(quantity[1:])
            return quantity
        except Exception as e:
            print(f"{Ticker} get quantity error ! {e}")
            time.sleep(1)
# Short Market Close
def closeMarketShort(Ticker,precision):
    while(True):
        try:
            quantity = round(getPositionQuantityShort(Ticker),precision)
            client.futures_create_order(symbol=Ticker, side="BUY", type="MARKET", quantity=quantity, positionSide="SHORT")
            break
        except Exception as e :
            print(f"{Ticker} closeShort error ! {e}")
            time.sleep(1)
# Get Order ID
def getOpenOrderID(Ticker):
    while(True):
        try:
            openOrders = client.futures_get_open_orders(symbol = Ticker)
            orderID = openOrders[0]["orderId"]
            return orderID
        except Exception as e :
            print(f"get open order error ! {e}")
# Close Order
def cancelOrderById(Ticker,orderID):
    while(True):
        try:
            client.futures_cancel_order(symbol=Ticker,orderId=orderID)
            break
        except Exception as e:
            print(f"cancel order error ! {e}") 
            time.sleep(1)
# Get position Avg price
def getAvgPrice(Ticker,OrderID):
    while(True):
        try:
            orderPrice = float(client.futures_get_order(symbol=Ticker,orderId=OrderID)["avgPrice"])
            return orderPrice
        except Exception as e:
            print(f"{Ticker} getAvgPrice error! {e}")
# Computing RSI Value
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
# Get RSI value
def getRSIValue(Ticker,Interval,Length):
    while(True):
        try:
            klines = client.futures_klines(symbol=Ticker, interval=Interval, limit='200') # "15m"
            close = [float(entry[4]) for entry in klines]
            close_array = np.asarray(close)
            rsiValue = computeRSI(close_array,Length) 
            return rsiValue
        except Exception as e:
            print(f"{Ticker} getRSIValue error ! {e}")
    

class MyWorker():
  def __init__(self,Ticker,Side,QtyDollar,Leverage,RSI_interval,RSI_Length,stopLossPercentage):
      
    self.Ticker = Ticker[:-4] # This will cut "PERP" string  BTCUSDTPERP => BTCUSDT
    self.Side = Side
    self.QtyDollar = QtyDollar  
    self.Leverage = Leverage
    self.RSI_interval = RSI_interval
    self.RSI_Length = RSI_Length
    self.stopLossPercentage = stopLossPercentage

    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):
    logging.info(self.Ticker,self)

    # Reading from Json
    Ticker = self.Ticker
    Side = self.Side
    QtyDollar = self.QtyDollar
    Leverage = self.Leverage
    RSI_interval = self.RSI_interval
    RSI_Length = self.RSI_Length
    stopLossPercentage = self.stopLossPercentage

    # Variables 
    global count
    count = 0

    # Setting for Leverage and Margin Type    
    ChangeLeverage(Ticker, Leverage)
    changeMarginType(Ticker, "ISOLATED")

    # Trade Algorithm
    if(Side=="LONG"): # If Buy signal 
        # Open Long Market Type
        currentPrice = getCurrentPrice(Ticker)
        precision = getPrecision(Ticker)
        leverage = Leverage
        qtyDollar = QtyDollar 
        quantity = round((qtyDollar/currentPrice*leverage),precision)
        OrderID = openMarketLong(Ticker, quantity)
        avgPrice = getAvgPrice(Ticker,OrderID) # Average Price
        while(count < 1): # Infinite Loop
            # Check if RSI is above 70
            rsiValue = getRSIValue(Ticker, RSI_interval, RSI_Length)
            currentPrice = getCurrentPrice(Ticker)
            priceDif = 100*(avgPrice-currentPrice)/avgPrice # Down percent
            print(priceDif)
            print(f"{Ticker} RSI Value: {rsiValue} priceDif:{priceDif}")
            if((rsiValue > 40) | (priceDif >= stopLossPercentage) ):
                # Close Long
                qtyLong = getPositionQuantityLong(Ticker)
                closeMarketLong(Ticker, precision)
                count = 1 # Break the while loop, Take profit, end the thread
            time.sleep(1) # Wait 1 sec
    elif(Side=="SHORT"): # If Sell signal 
        # Open Short Market Type
        currentPrice = getCurrentPrice(Ticker)
        precision = getPrecision(Ticker)
        leverage = Leverage
        qtyDollar = QtyDollar 
        quantity = round((qtyDollar/currentPrice*leverage),precision)
        OrderID = openMarketShort(Ticker, quantity)
        avgPrice = getAvgPrice(Ticker,OrderID) # Average price
        while(count < 1): # Infinite Loop
            # Check if RSI is below 30
            rsiValue = getRSIValue(Ticker, RSI_interval, RSI_Length)
            currentPrice = getCurrentPrice(Ticker)
            priceDif = 100*(currentPrice-avgPrice)/avgPrice # Up percent
            print(f"{Ticker} RSI Value: {rsiValue} priceDif:{priceDif}")
            if((rsiValue < 30) | (priceDif >= stopLossPercentage)):
                # Close Short
                qtyShort = getPositionQuantityShort(Ticker)
                closeMarketShort(Ticker, precision)
                count = 1 # Break the while loop, Take profit, end the thread
            time.sleep(1) # Wait 1 sec

@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template("info.html")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # POST Data
    try:
        data = json.loads(request.data)
        print(f"data:{data}")

        # Inputs from webhook message
        Ticker = data['TICKER']
        Side = data["SIDE"]
        QtyDollar = data["QTYDOLLAR"]
        Leverage = data["LEVERAGE"]
        RSI_interval = data["RSI_INTERVAL"]
        RSI_Length = data["RSI_LENGTH"]
        stopLossPercentage = data["STOPLOSSPERCENTAGE"]

        MyWorker(Ticker,Side,QtyDollar,Leverage,RSI_interval,RSI_Length,stopLossPercentage)
    except:
        pass
    
    return render_template("index.html")


#TO RUN OUR PYTHON APP
if __name__ =="__main__":
    app.run(debug=True)
    app.run(use_reloader=False, threaded=True)

# http://localhost:5000/webhook
# http://127.0.0.1:5000/webhook


