import os
import requests
from smartapi import SmartConnect
import pyotp

# GitHub/Replit ke "Secrets" se uthayega
API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

try:
    send_telegram("🤖 Bot Start ho raha hai")
    
    totp_input = input("Angel App ka TOTP dalo: ")

    smartApi = SmartConnect(api_key=API_KEY)
    data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp_input)

    if data['status']:
        print("Login Success")
        send_telegram("✅ Login Success Angel One")
    else:
        print("Login Fail:", data['message'])
        send_telegram("❌ Login Fail: " + data['message'])

except Exception as e:
    print("Error:", e)
    send_telegram("⚠️ Error: " + str(e))
