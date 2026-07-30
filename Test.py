import os
import logging
import requests
import pyotp
from smartapi import SmartConnect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read secrets from environment (do NOT hardcode)
API_KEY = os.environ.get("SMARTAPI_API_KEY")
CLIENT_CODE = os.environ.get("SMARTAPI_CLIENT_CODE")
PASSWORD = os.environ.get("SMARTAPI_PASSWORD")
TOTP_SECRET = os.environ.get("SMARTAPI_TOTP_SECRET")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(text: str, timeout: int = 10):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram token/chat id not configured in environment.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok") is True:
            logger.info("Telegram: message sent successfully")
            return True
        else:
            logger.error("Telegram API returned error: %s", data)
            return False
    except requests.RequestException as e:
        logger.exception("Telegram request failed: %s", e)
        return False

def angel_login():
    if not all([API_KEY, CLIENT_CODE, PASSWORD, TOTP_SECRET]):
        logger.error("SmartAPI credentials not fully configured in environment.")
        return None
    try:
        smart_api = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        logger.info("Generated TOTP (hidden in logs).")
        # generateSession behaviour may differ; check returned structure
        resp = smart_api.generateSession(CLIENT_CODE, PASSWORD, totp)
        logger.debug("SmartAPI raw response: %s", resp)
        status = str(resp.get("status", "")).lower()
        if status in ("success", "ok", "true", "200"):
            logger.info("Angel Login: success")
            return resp
        # sometimes API returns a 'data' or 'message' field
        logger.warning("Angel Login response: %s", resp.get("message", resp))
        return resp
    except Exception as e:
        logger.exception("Angel Login failed: %s", e)
        return None

if __name__ == "__main__":
    # 1) Test Telegram
    send_telegram_message("TEST 1: Telegram Chal Raha Hai")

    # 2) Test Angel Login
    login_resp = angel_login()
    if login_resp:
        logger.info("Login response keys: %s", list(login_resp.keys()))
    else:
        logger.error("Login failed; see previous logs.")
