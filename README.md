import numpy as np
import pandas as pd
from smc_ict_core import analyze, print_report

np.random.seed(42)

def make_ohlcv(n, freq, start="2026-01-01", trend=0.0002, vol=0.001):
    idx = pd.date_range(start, periods=n, freq=freq)
    returns = np.random.normal(trend, vol, n)
    close = 100 * np.cumprod(1 + returns)
    open_ = np.roll(close, 1)
    open_[0] = 100
    high = np.maximum(open_, close) * (1 + np.random.uniform(0, 0.001, n))
    low = np.minimum(open_, close) * (1 - np.random.uniform(0, 0.001, n))
    vol_col = np.random.randint(100, 1000, n)
    return pd.DataFrame({"Open": open_, "High": high, "Low": low, "Close": close,
                          "Volume": vol_col}, index=idx)

df_4h = make_ohlcv(200, "4h", trend=0.0015)
df_1h = make_ohlcv(400, "1h", trend=0.0015)
df_15m = make_ohlcv(500, "15min", trend=0.0015)
df_5m = make_ohlcv(500, "5min", trend=0.0015)
df_1m = make_ohlcv(500, "1min", trend=0.0015)

sig = analyze(df_4h, df_1h, df_15m, df_5m, df_1m)
print_report(sig)
# Robotic-ai.02

Ye Angel One + SMC/ICT Trading Bot hai jo Telegram par signal bhejta hai.

## Kaise Chalaye
1. `pip install numpy pandas requests`
2. `Main.py` me `TELEGRAM_TOKEN` aur `Angel One API` key dalo
3. `python Main.py` run karo

## Features
- SMC/ICT Analysis 4h, 1h, 15m, 5m, 1m
- Telegram Alert
- Angel One API Integration

## Link
GitHub: https://github.com/riteshsingh8155-ctrl/Robotic-ai.02
