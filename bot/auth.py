# bot/auth.py

import pyotp
import os
from dotenv import load_dotenv
from SmartApi import SmartConnect
# from Smartapi.smartConnect import SmartConnect

# Load environment variables
load_dotenv(dotenv_path="config/.env")

def generate_token():
    api_key = os.getenv("API_KEY")
    client_code = os.getenv("CLIENT_CODE")
    password = os.getenv("PASSWORD")
    totp_secret = os.getenv("TOTP_SECRET")

    if not all([api_key, client_code, password, totp_secret]):
        raise Exception("Missing credentials in .env file")

    # Create TOTP from secret
    totp = pyotp.TOTP(totp_secret).now()

    # Initialize connection
    obj = SmartConnect(api_key)
    data = obj.generateSession(client_code, password, totp)

    # Fetch access token
    refreshToken = data['data']['refreshToken']
    feedToken = obj.getfeedToken()
    accessToken = obj.getfeedToken()

    print("Login Success")
    return {
        "client_code": client_code,
        "obj": obj,
        "access_token": accessToken,
        "feed_token": feedToken
    }


# Test run
if __name__ == "__main__":
    session = generate_token()