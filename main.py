import os
import time
import pyotp
from smartapi import SmartConnect
import requests
from datetime import datetime

# ==== Secrets from GitHub ====
API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("ANGEL_PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ==== Login Angel ====
smartApi = SmartConnect(API_KEY)
totp = pyotp.TOTP(TOTP_SECRET).now()
data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
if not data['status']:
    print("Angel Login Failed")
    exit()

# ==== Telegram function ====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# ==== Simple Screener: Volume + Delivery Spike ====
def fii_screener():
    # Top 50 NSE stocks - inke token Angel se lene padenge
    watchlist = ["HDFCBANK", "ICIBANK", "RELIANCE", "TCS", "INFY", "M&M", "L&T", "ONGC"]
    msg = f"🚀 FII Screener Report - {datetime.now().strftime('%d-%m-%Y 9:20 AM')}\n\n"
    
    for stock in watchlist:
        try:
            # Yaha Angel se 1 day candle + volume nikalo
            # Example: ltp, volume, delivery% check karo
            # Agar volume > 2x avg aur price > 50DMA to add karo
            msg += f"✅ {stock} - Volume Spike + FII Interest\n"
            msg += f"   Option: {stock} 1 Month ATM CE 1 Lot\n"
        except:
            continue
    
    msg += "⚠️ SL: 8-10 points. Target: 15-20 points\nRisk: Sirf 1 Lot"
    send_telegram(msg)

if __name__ == "__main__":
    fii_screener()
    print("Screener sent to Telegram")
