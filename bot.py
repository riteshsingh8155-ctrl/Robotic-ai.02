import time
import pandas as pd
import talib
import numpy as np
from smartapi import SmartConnect
import pyotp
import requests
from datetime import datetime, timedelta

# ========== 1. YAHI APNA DATA BHAR DO ==========
API_KEY = "dOgfiXS0"
CLIENT_CODE = "APNA_CLIENT_CODE"
PASSWORD = "APNA_PASSWORD"
TOTP_SECRET = "APNA_TOTP_SECRET"

TELEGRAM_BOT_TOKEN = "APNA_BOT_TOKEN"
TELEGRAM_CHAT_ID = "APNA_CHAT_ID"
# =============================================

SYMBOLTOKEN = "26000"  # NIFTY 50. BANKNIFTY = 26009
SYMBOL = "NIFTY"
EXCHANGE = "NSE"
smartApi = None
last_signal = "WAIT"

def login():
    global smartApi
    try:
        totp = pyotp.TOTP(TOTP_SECRET).now()
        smartApi = SmartConnect(api_key=API_KEY)
        smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
        print(f"[{datetime.now()}] ✅ Angel Login Success")
    except Exception as e:
        print("Login Error:", e)

def get_candle_data(interval, days):
    try:
        params = {
            "exchange": EXCHANGE, "symboltoken": SYMBOLTOKEN, "interval": interval,
            "fromdate": (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M'),
            "todate": datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        res = smartApi.getCandleData(params)
        df = pd.DataFrame(res['data'], columns=['datetime','open','high','low','close','volume'])
        df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
        return df
    except Exception as e:
        print("Data Error:", e)
        return pd.DataFrame()

def check_indicators(df):
    if len(df) < 50: return False, False
    c = df['close']
    rsi = talib.RSI(c,14).iloc[-1]
    ema9 = talib.EMA(c,9).iloc[-1]
    ema21 = talib.EMA(c,21).iloc[-1]
    macd, macdsignal, _ = talib.MACD(c)
    macd = macd.iloc[-1]; macdsignal = macdsignal.iloc[-1]
    upper, _, lower = talib.BBANDS(c,20)
    upper = upper.iloc[-1]; lower = lower.iloc[-1]
    price = c.iloc[-1]
    
    buy = (rsi > 40 and rsi < 65) and (ema9 > ema21) and (macd > macdsignal) and (price > lower)
    sell = (rsi < 60 and rsi > 35) and (ema9 < ema21) and (macd < macdsignal) and (price < upper)
    return buy, sell

def get_oi_delta():
    try:
        data = smartApi.getOptionChainData({"exchange": EXCHANGE, "symboltoken": SYMBOLTOKEN})
        ce_vol = sum([i['volume'] for i in data['data'] if i['instrumenttype']=='CE'])
        pe_vol = sum([i['volume'] for i in data['data'] if i['instrumenttype']=='PE'])
        delta_vol = ce_vol - pe_vol
        
        if delta_vol > 500000: return "BULLISH_DELTA"
        if delta_vol < -500000: return "BEARISH_DELTA"
        return "NEUTRAL"
    except: return "NEUTRAL"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})
    except Exception as e: print("Telegram Error:", e)

login()
print(f"[{datetime.now()}] 🚀 Bot Started. Waiting for MTF Signal...")

while True:
    try:
        # 1. TREND CHECK - 1H + 30min
        df_1h = get_candle_data("ONE_HOUR", 10); buy_1h, sell_1h = check_indicators(df_1h)
        df_30 = get_candle_data("THIRTY_MINUTE", 5); buy_30, sell_30 = check_indicators(df_30)
        
        # 2. SIGNAL CHECK - 15min
        df_15 = get_candle_data("FIFTEEN_MINUTE", 3); buy_15, sell_15 = check_indicators(df_15)
        
        # 3. ENTRY CHECK - 1min
        df_1 = get_candle_data("ONE_MINUTE", 1); buy_1, sell_1 = check_indicators(df_1)
        
        # 4. OI/DELTA CHECK
        delta_status = get_oi_delta()
        
        final_signal = "WAIT"
        if buy_1h and buy_30 and buy_15 and buy_1 and delta_status=="BULLISH_DELTA":
            final_signal = "BUY"
        if sell_1h and sell_30 and sell_15 and sell_1 and delta_status=="BEARISH_DELTA":
            final_signal = "SELL"
        
        if final_signal!= "WAIT" and final_signal!= last_signal:
            price = df_1['close'].iloc[-1]
            msg = f"<b>🚨 AI MTF SIGNAL 🚨</b>\n\n<b>{final_signal}</b>\nSymbol: {SYMBOL}\nEntry TF: 1 Minute\nPrice: {price}\n\nTrend: 1H+30+15 ✅\nDelta: {delta_status} ✅"
            send_telegram(msg)
            print(f"[{datetime.now()}] {final_signal} SIGNAL SENT at {price}")
            last_signal = final_signal
        else:
            print(f"[{datetime.now()}] Waiting... Price: {df_1['close'].iloc[-1]}")
            
        time.sleep(30) # har 30 sec me check
        
    except Exception as e:
        print("Loop Error:", e)
        time.sleep(60)
    pip install smartapi-python pyotp pandas TA-Lib requests
