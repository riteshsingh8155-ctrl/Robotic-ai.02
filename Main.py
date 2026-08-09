import os
import requests
from smartapi import SmartConnect
import pyotp

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET") 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

try:
    totp = pyotp.TOTP(TOTP_SECRET).now() # input skip
    smartApi = SmartConnect(api_key=API_KEY)
    data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)

    if data['status']:
        send_telegram("✅ Angel One Login Success")
        print("Login Success")
    else:
        send_telegram("❌ Login Fail: " + data['message'])
        print("Login Fail")

except Exception as e:
    send_telegram("⚠️ Error: " + str(e))
    print("Error:", e)
import smartapi
print(smartapi.__version__)
