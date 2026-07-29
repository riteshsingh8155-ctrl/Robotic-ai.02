from smartapi import SmartConnect
import time
from datetime import datetime

API_KEY = "d0gfiXS0"
CLIENT_CODE = "YOUR_CLIENT_CODE"
PASSWORD = "YOUR_PASSWORD"
TOTP = "YOUR_TOTP"

SYMBOL = "NSE:NIFTY 50"  # Yaha BANKNIFTY bhi likh sakte ho
LOT_SIZE = 1
ENTRY_TIME = datetime.strptime("09:20", "%H:%M").time()

def login():
    obj = SmartConnect(api_key=API_KEY)
    data = obj.generateSession(CLIENT_CODE, PASSWORD, TOTP)
    return obj

def get_ltp(obj, symbol):
    ltp_data = obj.ltpData(exchange="NSE", tradingsymbol=symbol, symboltoken="99926000")
    return ltp_data['data']['ltp']

def check_setup(ltp, high, low):
    if ltp > high:
        return "BUY"
    elif ltp < low:
        return "SELL"
    return "NO_TRADE"

def place_order(obj, symbol, signal, qty):
    print(f"Order Placed: {signal} {qty} LOT of {symbol}")
    # Yaha apna order place ka code daalna

def main():
    obj = login()
    print("Bot Started... Waiting for 9:15")
    
    high_915_920 = 0
    low_915_920 = 999999
    trade_done = False
    
    while True:
        now = datetime.now().time()
        ltp = get_ltp(obj, SYMBOL)
        
        if now < ENTRY_TIME:
            if ltp > high_915_920: high_915_920 = ltp
            if ltp < low_915_920: low_915_920 = ltp
            print(f"Range: {low_915_920} - {high_915_920}")
        
        if now >= ENTRY_TIME and not trade_done:
            signal = check_setup(ltp, high_915_920, low_915_920)
            if signal != "NO_TRADE":
                place_order(obj, SYMBOL, signal, LOT_SIZE)
                trade_done = True
                print(f"Trade Taken: {signal}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
<script type="text/javascript">
new TradingView.widget({
  "width": "100%",
  "height": 610,
  "symbol": "NSE:NIFTY",
  "interval": "15", // 15 minute set
  "timezone": "Asia/Kolkata",
  "theme": "dark",
  "style": "1",
  "locale": "in",
  "toolbar_bg": "#1a1a1a",
  "studies": [ // Yaha indicator add hue
        "RSI@tv-basicstudies",
        "MASimple@tv-basicstudies",
        "MACD@tv-basicstudies",
        "BB@tv-basicstudies"
  ],
  "container_id": "tradingview_chart"
});
</script>
import time
import pandas as pd
import talib
from smartapi import SmartConnect
import pyotp
import requests
from datetime import datetime, timedelta

# ========== SETTINGS ==========
API_KEY = "TUMHARA_API_KEY"
CLIENT_CODE = "TUMHARA_CLIENT_CODE"
PASSWORD = "TUMHARA_PASSWORD"
TOTP_SECRET = "TUMHARA_TOTP_SECRET"

TELEGRAM_BOT_TOKEN = "APNA_BOT_TOKEN"
TELEGRAM_CHAT_ID = "APNA_CHAT_ID"

SYMBOLTOKEN = "26000" # NIFTY
SYMBOL = "NIFTY"
# ==============================

smartApi = None
last_signal = "WAIT"

def login():
    global smartApi
    totp = pyotp.TOTP(TOTP_SECRET).now()
    smartApi = SmartConnect(api_key=API_KEY)
    smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
    print("Angel Login Success")

def get_data(tf, days):
    params = {
        "exchange": "NSE", "symboltoken": SYMBOLTOKEN,
        "interval": tf, # "ONE_HOUR", "THIRTY_MINUTE", "FIFTEEN_MINUTE", "ONE_MINUTE"
        "fromdate": (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M'),
        "todate": datetime.now().strftime('%Y-%m-%d %H:%M')
    }
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

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

login()
while True:
    # 1. BADA TF CHECK - 1H aur 30min
    df_1h = get_data("ONE_HOUR", 10)
    df_30 = get_data("THIRTY_MINUTE", 5)
    buy_1h, sell_1h = check_indicators(df_1h)
    buy_30, sell_30 = check_indicators(df_30)

    # 2. SIGNAL TF CHECK - 15min
    df_15 = get_data("FIFTEEN_MINUTE", 3)
    buy_15, sell_15 = check_indicators(df_15)

    # 3. ENTRY TF - 1min me final trigger
    df_1 = get_data("ONE_MINUTE", 1)
    buy_1, sell_1 = check_indicators(df_1)
    
    final_signal = "WAIT"
    if buy_1h and buy_30 and buy_15 and buy_1:
        final_signal = "BUY"
    if sell_1h and sell_30 and sell_15 and sell_1:
        final_signal = "SELL"
    
    if final_signal!= "WAIT" and final_signal!= last_signal:
        price = df_1['close'].iloc[-1]
        msg = f"<b>🚨 MTF AI SIGNAL 🚨</b>\n\n<b>{final_signal}</b>\nSymbol: {SYMBOL}\nEntry TF: 1min\nPrice: {price}\n\nTrend: 1H+30min+15min Confirmed"
        send_telegram(msg)
        print(f"{datetime.now()} - {final_signal} at {price}")
        last_signal = final_signal

    time.sleep(30) # har 30 sec me 1min check karega
