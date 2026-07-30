import pyotp, time, requests, pandas as pd
from smartapi import SmartConnect
from datetime import datetime

# ======= YAHAN APNA DATA 100% SAHI DAALO =======
API_KEY = "dOgfiXS0"
CLIENT_CODE = "R1001550"
PASSWORD = "2002"
TOTP_SECRET = "ANGEL_APP_SE_NAYA_TOTP_COPY_KARO" # Har 30 sec me badalta hai
TELEGRAM_BOT_TOKEN = "8534769215:AAGSTXW_0gztZk9qcSoTCiQa819YWoiXVX8" # Naya wala
TELEGRAM_CHAT_ID = "8872099638" # Tumhara ID
# ========================================

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    r = requests.post(url, data=data)
    print("Telegram Status:", r.json()['ok'])

def get_data(smart, symbol, token):
    try:
        ltp = smart.ltpData(exchange="NSE", tradingsymbol=symbol, symboltoken=token)
        return float(ltp['data']['ltp'])
    except: 
        return 0

def check_ai_signal(price):
    # Simple AI Logic: Price 100 ka multiple tode to signal
    if price > 77800:
        return "BUY", 4, "STRONG"
    elif price < 77600:
        return "SELL", 4, "STRONG"
    else:
        return "WAIT", 2, "SIDEWAYS"

def login_angel():
    smartApi = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp)
    if data['status']:
        send_telegram("✅ Bot ON ho gaya + Angel Login Success")
        return smartApi
    else:
        send_telegram("❌ Angel Login Fail: " + data['message'])
        return None

def main():
    smart = login_angel()
    if not smart: return

    while True:
        try:
            # BANKNIFTY ka LTP le rahe
            price = get_data(smart, "BANKNIFTY", "26000") 
            
            signal, score, status = check_ai_signal(price)
            
            if signal != "WAIT": # Sirf tab message bhejo jab signal bane
                msg = f"""🚨 AI सिग्नल: BANKNIFTY
सिग्नल: {signal}
Score: {score}/4
स्टेटस: {status}
LTP: {price}
Time: {datetime.now().strftime('%H:%M:%S')}"""
                send_telegram(msg)
            
            print(f"LTP: {price} | Signal: {signal}")
            time.sleep(30) # 30 sec me check karega

        except Exception as e:
            print("Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    main()
