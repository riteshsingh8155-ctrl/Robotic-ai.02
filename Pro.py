import time
import pandas as pd
import talib
from smartapi import SmartConnect
import pyotp
import requests
from datetime import datetime, timedelta

# ========== YAHI 5 DETAIL BHAR DO ==========
API_KEY = "dOgfiXS0"
CLIENT_CODE = "TUMHARA_CLIENT_CODE"
PASSWORD = "TUMHARA_PASSWORD" 
TOTP_SECRET = "TUMHARA_TOTP_SECRET"

TELEGRAM_BOT_TOKEN = "TUMHARA_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TUMHARA_CHAT_ID"
# ===========================================

SYMBOLTOKEN = "26000" # NIFTY
smartApi = None
last_signal = "WAIT"

def login():
    global smartApi
    totp = pyotp.TOTP(TOTP_SECRET).now()
    smartApi = SmartConnect(api_key=API_KEY)
    smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
    print("✅ Angel Login Success")

def get_data(tf, days):
    params = {"exchange": "NSE", "symboltoken": SYMBOLTOKEN, "interval": tf,
              "fromdate": (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M'),
              "todate": datetime.now().strftime('%Y-%m-%d %H:%M')}
    res = smartApi.getCandleData(params)
    df = pd.DataFrame(res['data'], columns=['dt','open','high','low','close','volume'])
    df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
    return df

def check_indicators(df):
    c = df['close']
    rsi = talib.RSI(c,14).iloc[-1]
    ema9 = talib.EMA(c,9).iloc[-1]
    ema21 = talib.EMA(c,21).iloc[-1]
    macd, macdsignal, _ = talib.MACD(c)
    macd = macd.iloc[-1]; macdsignal = macdsignal.iloc[-1]
    upper, _, lower = talib.BBANDS(c,20)
    upper = upper.iloc[-1]; lower = lower.iloc[-1]
    price = c.iloc[-1]
    buy = rsi>40 and ema9>ema21 and macd>macdsignal and price>lower
    sell = rsi<60 and ema9<ema21 and macd<macdsignal and price<upper
    return buy, sell

def get_delta():
    try:
        data = smartApi.getOptionChainData({"exchange": "NSE", "symboltoken": SYMBOLTOKEN})
        ce_vol = sum([i['volume'] for i in data['data'] if i['instrumenttype']=='CE'])
        pe_vol = sum([i['volume'] for i in data['data'] if i['instrumenttype']=='PE'])
        delta = ce_vol - pe_vol
        if delta > 500000: return "BULLISH"
        if delta < -500000: return "BEARISH"
        return "NEUTRAL"
    except: return "NEUTRAL"

def send(msg):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                  data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

login()
while True:
    df_1h = get_data("ONE_HOUR", 10); b1h, s1h = check_indicators(df_1h)
    df_30 = get_data("THIRTY_MINUTE", 5); b30, s30 = check_indicators(df_30)
    df_15 = get_data("FIFTEEN_MINUTE", 3); b15, s15 = check_indicators(df_15)
    df_1 = get_data("ONE_MINUTE", 1); b1, s1 = check_indicators(df_1)
    delta = get_delta()
    
    signal = "WAIT"
    if b1h and b30 and b15 and b1 and delta=="BULLISH": signal = "BUY"
    if s1h and s30 and s15 and s1 and delta=="BEARISH": signal = "SELL"
    
    if signal!= "WAIT" and signal!= last_signal:
        msg = f"🚨 AI SIGNAL 🚨\n{signal}\nNIFTY @ {df_1['close'].iloc[-1]}\nTF: 1min Entry | Delta: {delta}"
        send(msg); print(f"{datetime.now()} - {signal}"); last_signal = signal
    time.sleep(30)
