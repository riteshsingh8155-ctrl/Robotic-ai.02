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
