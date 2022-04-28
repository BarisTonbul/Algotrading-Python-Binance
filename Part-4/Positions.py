from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import time

from selenium import webdriver
from selenium.webdriver.common.proxy import *

import threading, config
from Bots import shortPosition,longPosition,getPrecision,openPositions
#---------------------------------------------------------------------------------------------------------------------------------

qty1_Dollar = 2.5 # First buy cumQty
qty2_Dollar = 2.5 # Second buy cumQty

leverageLong = 50 # Leverage for long
leverageShort = 50 # Leverage for short

rsi1Long = 21
rsi2Long = 19

rsi1Short = 68
rsi2Short = 85

tradingview_Mail = config.mail
tradingview_Password = config.password
#---------------------------------------------------------------------------------------------------------------------------------
# Long Screener
def longPositionFunc():
    # Defining browser
    openTradingview = webdriver.Firefox()
    openTradingview.get("https://www.tradingview.com/")
    openTradingview.maximize_window() # Fullscreen mode
    while(True):
        try:
            # Log in 
            account_Btn_XPATH = "/html/body/div[2]/div[3]/div[2]/div[3]/button[1]" 
            account_Btn = openTradingview.find_element(By.XPATH, account_Btn_XPATH)
            account_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            login_Btn_XPATH = "/html/body/div[6]/div/span/div[1]/div/div/div[1]"
            login_Btn = openTradingview.find_element(By.XPATH, login_Btn_XPATH)
            login_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Select via mail
            mail_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div"
            mail_Btn = openTradingview.find_element(By.XPATH, mail_Btn_XPATH)
            mail_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Mail inputs
            mailDiv_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[1]/div[1]"
            mailDiv_Btn = openTradingview.find_element(By.XPATH, mailDiv_Btn_XPATH)
            mailDiv_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            email_input_XPATH = "username"
            email_input = openTradingview.find_element(By.NAME, email_input_XPATH)
            email_input.send_keys(config.mail)
            break
        except:
            pass
    while(True):
        try:
            passDiv_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[2]/div[1]"
            passDiv_Btn = openTradingview.find_element(By.XPATH, passDiv_Btn_XPATH)
            passDiv_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            password_input_XPATH = "password"
            password_input = openTradingview.find_element(By.NAME, password_input_XPATH)
            password_input.click()
            password_input.send_keys(config.password)
            break
        except:
            pass
    while(True):
        try:
            # Log in Button
            login_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[5]/div[2]"
            login_Btn = openTradingview.find_element(By.XPATH, login_Btn_XPATH)
            login_Btn.click()
            time.sleep(10)
            break
        except:
            pass
    time.sleep(3)
    # Go to screener page
    openTradingview.get("https://tradingview.com/crypto-screener/")
    while(True):
        try:
            # Filter Button
            filter_Btn_XPATH = "/html/body/div[4]/div/div[2]/div[13]"
            filter_Btn = openTradingview.find_element(By.XPATH, filter_Btn_XPATH)  
            filter_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Search for RSI 
            search_input_XPATH = "/html/body/div[8]/div/div/div/div[2]/input"
            search_input = openTradingview.find_element(By.XPATH, search_input_XPATH)  
            search_input.send_keys("RSI")
            break
        except:
            pass
    while(True):
        try:
            # Below button for RSI
            below_Btn_XPATH = "/html/body/div[8]/div/div/div/div[3]/div[1]/div/div/div[45]/div[2]/label[1]/span/span"
            below_Btn =  openTradingview.find_element(By.XPATH, below_Btn_XPATH)
            below_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Seleck below button
            belowOrEqual_Btn_XPATH = "/html/body/div[8]/div/div/div/div[4]/div/div[1]/span[1]/span"
            belowOrEqual_Btn = openTradingview.find_element(By.XPATH, belowOrEqual_Btn_XPATH)
            belowOrEqual_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Value Input
            value_Inp_XPATH = "/html/body/div[8]/div/div/div/div[3]/div[1]/div/div/div[45]/div[2]/input[1]"
            value_Inp = openTradingview.find_element(By.XPATH, value_Inp_XPATH)
            value_Inp.send_keys(30)
            break
        except:
            pass
    while(True):
        try:
            # Search for Exchange
            search_input_XPATH = "/html/body/div[8]/div/div/div/div[2]/input"
            search_input = openTradingview.find_element(By.XPATH, search_input_XPATH)  
            search_input.clear()
            search_input.send_keys("exchange")
            break
        except:
            pass
    while(True):
        try:
            # Exchange option button
            exchange_Btn_XPATH = "/html/body/div[8]/div/div/div/div[3]/div[1]/div/div/div[1]/div[2]/div/span/span"
            exchange_Btn = openTradingview.find_element(By.XPATH, exchange_Btn_XPATH) 
            exchange_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Select Binance
            binanceExchange_Btn_XPATH = "/html/body/div[8]/div/div/div/div[4]/div[3]/div[1]/div[3]/label/label/span[2]"
            binanceExchange_Btn = openTradingview.find_element(By.XPATH, binanceExchange_Btn_XPATH) 
            binanceExchange_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Close Btn
            close_Btn_XPATH = "/html/body/div[8]/div/div/div/div[1]/div[3]"
            close_Btn = openTradingview.find_element(By.XPATH, close_Btn_XPATH)     
            close_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Time Interval Btn
            interval_Btn_XPATH = "/html/body/div[4]/div/div[2]/div[7]/div[2]"
            interval_Btn = openTradingview.find_element(By.XPATH, interval_Btn_XPATH) 
            interval_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # 15 minutes button
            interval15min_Btn_XPATH = "/html/body/div[4]/div/div[2]/div[7]/div[3]/div/div[1]/div[3]/div"
            interval15min_Btn = openTradingview.find_element(By.XPATH, interval15min_Btn_XPATH) 
            interval15min_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Perp text input
            text_input_XPATH = "//*[@id='js-screener-container']/div[3]/table/thead/tr/th[1]/div/div/div[3]/input"
            text_input = openTradingview.find_element(By.XPATH, text_input_XPATH) 
            text_input.send_keys("usdtperp")
            break
        except:
            pass
    time.sleep(5)        
    while(True):
        for i in range(1,2):
            try:               
                symbolName_XPATH = f"/html/body/div[4]/div/div[4]/table/tbody/tr[{i}]/td[1]/div/div[2]/a"
                symbolName = openTradingview.find_element(By.XPATH, symbolName_XPATH).text
                Ticker = symbolName[:-4]
                if (openPositions.get(f"{Ticker}")==None): # Bot will start following rsi value
                    # Threads
                    LongThread = threading.Thread(target=longPosition,args=(Ticker,getPrecision(Ticker),leverageLong,qty1_Dollar,qty2_Dollar,rsi1Long,rsi2Long))
                    LongThread.start()
                    openPositions[Ticker] = "started"
                    #print(f"{i}. Satir, {Ticker} Long takip ediliyor")
                else: # Bot already runnning
                    print(f"{Ticker} has already started")
                    pass
            except Exception as e :
                #print(f"{i}. Satir alinamadi...")
                pass
        time.sleep(3)

# Short Screener
def shortPositionFunc():
    # Defining browser
    openTradingview = webdriver.Firefox()
    openTradingview.get("https://www.tradingview.com/")
    openTradingview.maximize_window() # Fullscreen mode
    while(True):
        try:
            # Log in 
            account_Btn_XPATH = "/html/body/div[2]/div[3]/div[2]/div[3]/button[1]" 
            account_Btn = openTradingview.find_element(By.XPATH, account_Btn_XPATH)
            account_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            login_Btn_XPATH = "/html/body/div[6]/div/span/div[1]/div/div/div[1]"
            login_Btn = openTradingview.find_element(By.XPATH, login_Btn_XPATH)
            login_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Select via mail
            mail_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div"
            mail_Btn = openTradingview.find_element(By.XPATH, mail_Btn_XPATH)
            mail_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Mail inputs
            mailDiv_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[1]/div[1]"
            mailDiv_Btn = openTradingview.find_element(By.XPATH, mailDiv_Btn_XPATH)
            mailDiv_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            email_input_XPATH = "username"
            email_input = openTradingview.find_element(By.NAME, email_input_XPATH)
            email_input.send_keys(config.mail)
            break
        except:
            pass
    while(True):
        try:
            passDiv_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[2]/div[1]"
            passDiv_Btn = openTradingview.find_element(By.XPATH, passDiv_Btn_XPATH)
            passDiv_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            password_input_XPATH = "password"
            password_input = openTradingview.find_element(By.NAME, password_input_XPATH)
            password_input.click()
            password_input.send_keys(config.password)
            break
        except:
            pass
    while(True):
        try:
            # Log in Button
            login_Btn_XPATH = "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[5]/div[2]"
            login_Btn = openTradingview.find_element(By.XPATH, login_Btn_XPATH)
            login_Btn.click()
            time.sleep(10)
            break
        except:
            pass
    time.sleep(3)
    # Go to screener page
    openTradingview.get("https://tradingview.com/crypto-screener/")
    while(True):
        try:
            # Filter Button
            filter_Btn_XPATH = "/html/body/div[4]/div/div[2]/div[13]"
            filter_Btn = openTradingview.find_element(By.XPATH, filter_Btn_XPATH)  
            filter_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Search for RSI 
            search_input_XPATH = "/html/body/div[8]/div/div/div/div[2]/input"
            search_input = openTradingview.find_element(By.XPATH, search_input_XPATH)  
            search_input.send_keys("RSI")
            break
        except:
            pass
    while(True):
        try:
            # Below button for RSI
            below_Btn_XPATH = "/html/body/div[8]/div/div/div/div[3]/div[1]/div/div/div[45]/div[2]/label[1]/span/span"
            below_Btn =  openTradingview.find_element(By.XPATH, below_Btn_XPATH)
            below_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Seleck above button
            aboveOrEqual_Btn_XPATH = "/html/body/div[8]/div/div/div/div[4]/div/div[1]/span[3]/span"
            aboveOrEqual_Btn = openTradingview.find_element(By.XPATH, aboveOrEqual_Btn_XPATH)
            aboveOrEqual_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Value Input
            value_Inp_XPATH = "/html/body/div[8]/div/div/div/div[3]/div[1]/div/div/div[45]/div[2]/input[1]"
            value_Inp = openTradingview.find_element(By.XPATH, value_Inp_XPATH)
            value_Inp.send_keys(70)
            break
        except:
            pass
    while(True):
        try:
            # Search for Exchange
            search_input_XPATH = "/html/body/div[8]/div/div/div/div[2]/input"
            search_input = openTradingview.find_element(By.XPATH, search_input_XPATH)  
            search_input.clear()
            search_input.send_keys("exchange")
            break
        except:
            pass
    while(True):
        try:
            # Exchange option button
            exchange_Btn_XPATH = "/html/body/div[8]/div/div/div/div[3]/div[1]/div/div/div[1]/div[2]/div/span/span"
            exchange_Btn = openTradingview.find_element(By.XPATH, exchange_Btn_XPATH) 
            exchange_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Select Binance
            binanceExchange_Btn_XPATH = "/html/body/div[8]/div/div/div/div[4]/div[3]/div[1]/div[3]/label/label/span[2]"
            binanceExchange_Btn = openTradingview.find_element(By.XPATH, binanceExchange_Btn_XPATH) 
            binanceExchange_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Close Btn
            close_Btn_XPATH = "/html/body/div[8]/div/div/div/div[1]/div[3]"
            close_Btn = openTradingview.find_element(By.XPATH, close_Btn_XPATH)     
            close_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Time Interval Btn
            interval_Btn_XPATH = "/html/body/div[4]/div/div[2]/div[7]/div[2]"
            interval_Btn = openTradingview.find_element(By.XPATH, interval_Btn_XPATH) 
            interval_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # 15 minutes button
            interval15min_Btn_XPATH = "/html/body/div[4]/div/div[2]/div[7]/div[3]/div/div[1]/div[3]/div"
            interval15min_Btn = openTradingview.find_element(By.XPATH, interval15min_Btn_XPATH) 
            interval15min_Btn.click()
            break
        except:
            pass
    while(True):
        try:
            # Perp text input
            text_input_XPATH = "//*[@id='js-screener-container']/div[3]/table/thead/tr/th[1]/div/div/div[3]/input"
            text_input = openTradingview.find_element(By.XPATH, text_input_XPATH) 
            text_input.send_keys("usdtperp")
            break
        except:
            pass
    time.sleep(5)        
    while(True):
        for i in range(1,2):
            try:               
                symbolName_XPATH = f"/html/body/div[4]/div/div[4]/table/tbody/tr[{i}]/td[1]/div/div[2]/a"
                symbolName = openTradingview.find_element(By.XPATH, symbolName_XPATH).text
                Ticker = symbolName[:-4]
                if (openPositions.get(f"{Ticker}")==None): # Bot will start following rsi value
                    # Threads
                    shortThread = threading.Thread(target=shortPosition,args=(Ticker,getPrecision(Ticker),leverageShort,qty1_Dollar,qty2_Dollar,rsi1Short,rsi2Short))
                    shortThread.start()
                    openPositions[Ticker] = "started"
                    #print(f"{i}. Satir, {Ticker} Long takip ediliyor")
                else: # Bot already runnning
                    print(f"{Ticker} has already started")
                    pass
            except Exception as e :
                #print(f"{i}. Satir alinamadi...")
                pass
        time.sleep(3)



# Long screener thread
longPositionBot = threading.Thread(target=longPositionFunc,args=())
#longPositionBot.start()

# Short screener thread
shortPositionBot = threading.Thread(target=shortPositionFunc,args=())
shortPositionBot.start()