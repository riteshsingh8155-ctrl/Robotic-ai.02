import pandas as pd
import pandas_ta as ta
import yfinance as yf
import requests
import time
from datetime import datetime

# ===== 1. SETTINGS YAHAN BADAL =====
SYMBOL = "XAUUSD=X"  # GOLD. Silver: SI=F  |  BTC: BTC-USD
TELEGRAM_TOKEN = "8534769215:AAGSTXW_0gztZk9qcSoTCiQa819YWoiXVX8"
TELEGRAM_CHAT_ID = "8872099638"
RISK_REWARD = 2.5
SCAN_EVERY_SECONDS = 300  # 5 min me 1 bar check karega
# ====================================

last_signal_time = None

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram Error:", e)

def get_data(symbol, interval, period):
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        df.dropna(inplace=True)
        return df
    except:
        return pd.DataFrame()

def find_fvg(df):
    df['FVG_Bull'] = (df['Low'] > df['Low'].shift(2)) & (df['High'].shift(2) < df['Low'])
    df['FVG_Bear'] = (df['High'] < df['High'].shift(2)) & (df['Low'].shift(2) > df['High'])
    return df

def check_bos(df):
    df['BOS_Bull'] = df['Close'] > df['High'].shift(1)
    df['BOS_Bear'] = df['Close'] < df['Low'].shift(1)
    return df

def run_strategy():
    global last_signal_time
    print("Scanning...", datetime.now().strftime("%H:%M:%S"))
    
    # Step 1: 4H Range = Accumulation
    df_4h = get_data(SYMBOL, "4h", "60d")
    if df_4h.empty: return
    range_high = df_4h['High'][-20:].max()
    range_low = df_4h['Low'][-20:].min()
    price_4h = df_4h['Close'][-1]
    bias = "BULLISH" if price_4h > range_high else "BEARISH" if price_4h < range_low else "RANGE"
    
    # Step 2: 1H Manipulation
    df_1h = get_data(SYMBOL, "1h", "30d")
    if df_1h.empty: return
    manipulation_bull = df_1h['Low'][-1] < range_low and df_1h['Close'][-1] > range_low
    manipulation_bear = df_1h['High'][-1] > range_high and df_1h['Close'][-1] < range_high
    
    # Step 3: 15M FVG
    df_15m = get_data(SYMBOL, "15m", "10d")
    if df_15m.empty: return
    df_15m = find_fvg(df_15m)
    
    # Step 4: 5M BOS Entry
    df_5m = get_data(SYMBOL, "5m", "5d")
    if df_5m.empty: return
    df_5m = check_bos(df_5m)
    
    last_5m = df_5m.iloc[-1]
    last_15m = df_15m.iloc[-1]
    
    # Duplicate signal rokne ke liye
    current_candle_time = last_5m.name
    
    # ===== BUY SIGNAL =====
    if manipulation_bull and last_15m['FVG_Bull']
