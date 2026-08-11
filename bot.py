import os
from smartapi import SmartConnect
import pyotp
from dotenv import load_dotenv

load_dotenv() # .env file load karega

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
PASSWORD = os.getenv("ANGEL_PASSWORD")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")

def login_angel():
    try:
        # TOTP generate hoga har 30 sec me
        totp = pyotp.TOTP(TOTP_SECRET).now()
        
        obj = SmartConnect(api_key=API_KEY)
        data = obj.generateSession(CLIENT_CODE, PASSWORD, totp)
        
        if data['status']:
            print("Login Success!")
            return obj
        else:
            print("Login Failed:", data)
            return None
    except Exception as e:
        print("Error:", e)
        return None

def get_ltp(obj, symbol):
    try:
        ltp_data = obj.ltpData(exchange="NSE", tradingsymbol=symbol, symboltoken="")
        print(f"{symbol} LTP: {ltp_data['data']['ltp']}")
        return ltp_data['data']['ltp']
    except Exception as e:
        print("LTP Error:", e)

if __name__ == "__main__":
    angel = login_angel()
    if angel:
        get_ltp(angel, "SYRMA SGS EQ")
