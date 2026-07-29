9o⁸import time
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
    pip install smartapi-python pyotp pandas TA-Lib requests
    python Pro.py
CLIENT_CODE = "TUMHARA_ANGEL_ID"
PASSWORD = "TUMHARA_PASSWORD" 
TOTP_SECRET = "TUMHARA_TOTP"
TELEGRAM_BOT_TOKEN = "TUMHARA_TOKEN"
TELEGRAM_CHAT_ID = "TUMHARA_CHAT_ID"
def get_ltp(obj, symboltoken): 
    try: 
        ltp_data = obj.ltpData(exchange="NSE", tradingsymbol="NIFTY 50", symboltoken="99926000") 
        return ltp_data['data']['ltp'] 
    except: 
        return 0
import pyotp
import time
from smartapi import SmartConnect
import requests

# ======= APNE DETAILS YAHAN DAALO =======
API_KEY = "dOgfiXS0"
CLIENT_CODE = "R1001550"
PASSWORD = "2002"  # Tumhara naya password
TOTP_SECRET = "TUMHARA_NAYA_TOTP_SECRET"  # Angel se mila hua
TELEGRAM_BOT_TOKEN = "8534769215:AAGSTXW_0gztZk9qcSoTCiQa819YWoiXVX8"  # BotFather se naya
TELEGRAM_CHAT_ID = "8872099638"
# ========================================

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=data)

def login_angel():
    smartApi = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
    
    if data['status']:
        send_telegram("✅ Angel Login Success")
        return smartApi
    else:
        send_telegram("❌ Angel Login Failed: " + str(data['message']))
        return None

def main():
    send_telegram("🚀 Pro.py Bot Started")
    smart = login_angel()
    
    if smart:
        # Yahan apna trading logic likhna
        # Example: har 60 sec me balance check
        while True:
            try:
                balance = smart.rmsLimit()
                send_telegram(f"Balance: {balance}")
                time.sleep(60)
            except Exception as e:
                send_telegram(f"Error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    main()
INDEX:NSEI
INDEX:NSEBANK
import requests
from datetime import datetime

SECTORS = {
    "BANK": ["HDFCBANK", "ICIBANK", "SBIN", "KOTAKBANK", "AXISBANK"],
    "IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM"],
    "AUTO": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "HEROMOTOCO"]
}

def get_sector_change(smart, sector_stocks):
    # Sector ka avg change nikalega
    total_change = 0
    for stock in sector_stocks:
        data = smart.ltpData(exchange="NSE", tradingsymbol=stock, symboltoken="")
        total_change += data['data']['change']
    return total_change / len(sector_stocks)

def find_smart_money_stock(smart, sector_name, sector_stocks):
    for stock in sector_stocks:
        try:
            ltp_data = smart.ltpData(exchange="NSE", tradingsymbol=stock, symboltoken="")
            ohlc = smart.getCandleData(...) # Yahan OI + Volume nikalna padega
            
            price_change = ltp_data['data']['change']
            volume = ltp_data['data']['volume']
            oi_change = 15 # Yahan Angel se OI % laana padega
            
            # CONDITION: OI badi + Price badi + Volume zyada
            if oi_change > 10 and price_change > 1.5 and volume > 1000000:
                msg = f"""🚨 SMART MONEY SIGNAL
Sector: {sector_name} 🔥
Stock: {stock}
Price: {ltp_data['data']['ltp']}
Price Change: {price_change}%
OI Change: +{oi_change}%
Volume: {volume}
Reason: Sector Top + OI Spike + Volume Spike
Time: {datetime.now().strftime('%H:%M:%S')}"""
                send_telegram(msg)
        except:
            pass

def main():
    smart = login_angel()
    while True:
        # 1. Sabse garm/thanda sector dhoondo
        hottest_sector = "BANK" # Logic se nikalega
        find_smart_money_stock(smart, hottest_sector, SECTORS[hottest_sector])
        time.sleep(300) # 5 min me 1 baar check
import pyotp, time, requests
from smartapi import SmartConnect
from datetime import datetime

# ======= APNE DETAILS DAALO =======
API_KEY = "dOgfiXS0"
CLIENT_CODE = "R1001550"
PASSWORD = "2002"
TOTP_SECRET = "TUMHARA_NAYA_TOTP_SECRET"
TELEGRAM_BOT_TOKEN = "8534769215:AAGSTXW_0gztZk9qcSoTCiQa819YWoiXVX8"
TELEGRAM_CHAT_ID = "8872099638"
# ========================================

# SECTOR LIST - F&O stocks hi daalo jisme OI milega
SECTORS = {
    "BANK": ["HDFCBANK", "ICIBANK", "SBIN", "KOTAKBANK", "AXISBANK", "BANKNIFTY"],
    "IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM", "NIFTYIT"],
    "AUTO": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "HEROMOTOCO"]
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def login_angel():
    smartApi = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
    if data['status']: 
        send_telegram("✅ Bot Started + Login Success")
        return smartApi
    else: 
        send_telegram("❌ Login Failed")
        return None

def get_oi_data(smart, symbol):
    # F&O ka OI nikalne ke liye
    try:
        data = smart.getOptionChain(symbol=symbol, strikePrice=0, expiryDate="")
        # Yahan ATM call+put ka OI total kar sakte ho
        # Simple ke liye hum ltp + volume + change le rahe
        ltp = smart.ltpData(exchange="NSE", tradingsymbol=symbol, symboltoken="")
        return ltp['data']
    except:
        return None

def main():
    smart = login_angel()
    if not smart: return

    while True:
        try:
            # 1. Sabse tez sector dhoondo
            for sector, stocks in SECTORS.items():
                sector_change = 0
                for s in stocks:
                    d = get_oi_data(smart, s)
                    if d: sector_change += d['change']
                sector_change = sector_change / len(stocks)

                # 2. Agar sector 1.5% se zyada hila to usme stock dhoondo
                if abs(sector_change) > 1.5:
                    for stock in stocks:
                        d = get_oi_data(smart, stock)
                        if d and d['volume'] > 500000: # Volume filter
                            # 3. Yahan OI logic - Angel se direct OI nahi aata to hum volume + price se smart money pakadte
                            if d['change'] > 2 and sector_change > 0: # Upar wala sector
                                msg = f"""🚨 SMART MONEY BUY
Sector: {sector} +{round(sector_change,2)}%
Stock: {stock}
Price: {d['ltp']}
Change: +{d['change']}%
Volume: {d['volume']}
Note: OI spike check karne ke liye Angel App me iska F&O dekho
Time: {datetime.now().strftime('%H:%M:%S')}"""
                                send_telegram(msg)
            
            time.sleep(300) # 5 min baad dubara check
        except Exception as e:
            send_telegram(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
