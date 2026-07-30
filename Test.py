import requests
import pyotp
from smartapi import SmartConnect

API_KEY = "dOgfiXS0"
CLIENT_CODE = "R1001550"
PASSWORD = "2002"
TOTP_SECRET = "TUMHARA_NAYA_TOTP_SECRET"
TELEGRAM_BOT_TOKEN = "8534769215:AAGSTXW_0gztZk9qcSoTCiQa819YWoiXVX8"
TELEGRAM_CHAT_ID = "8872099638"

# 1. Telegram Test
r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
data={"chat_id": TELEGRAM_CHAT_ID, "text": "TEST 1: Telegram Chal Raha Hai"})
print("Telegram:", r.text)

# 2. Angel Login Test
smartApi = SmartConnect(api_key=API_KEY)
totp = pyotp.TOTP(TOTP_SECRET).now()
data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
print("Angel Login:", data['status'], data.get('message'))
