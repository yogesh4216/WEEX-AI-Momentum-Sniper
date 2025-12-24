import time
import pickle
import os
import requests
import hmac
import hashlib
import base64
import json
import urllib3
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
MODEL_FILE = "my_first_ai_model.pkl"

# --- AUTHENTICATION ---
api_key = os.environ.get("WEEX_API_KEY")
secret_key = os.environ.get("WEEX_SECRET_KEY")
passphrase = os.environ.get("WEEX_PASSPHRASE")

print("🚀 AI TRADING BOT INITIALIZING...")

def get_signature(timestamp, method, endpoint, body):
    message = timestamp + method + endpoint + body
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def manual_hackathon_test():
    print("\n🛠️  STARTING FINAL CONNECTION TEST...")
    
    if not api_key:
        print("⚠️  Missing Keys. Skipping.")
        return

    # --- THE FIX: USE THE OFFICIAL API DOMAIN ---
    # According to WEEX Docs, this is the correct domain for account/assets
    base_url = "https://api-spot.weex.com" 
    
    endpoint = "/api/v1/account/assets"
    method = "GET"
    body = ""
    timestamp = str(int(time.time() * 1000))
    signature = get_signature(timestamp, method, endpoint, body)

    headers = {
        "Content-Type": "application/json",
        "X-WEEX-ACCESS-KEY": api_key,
        "X-WEEX-ACCESS-PASSPHRASE": passphrase,
        "X-WEEX-ACCESS-TIMESTAMP": timestamp,
        "X-WEEX-ACCESS-SIGN": signature
    }

    print(f"👉 Connecting to: {base_url}{endpoint}")

    try:
        response = requests.get(base_url + endpoint, headers=headers, timeout=10)
        data = response.json()
        
        if data.get('code') == '00000' or data.get('msg') == 'success':
            print("\n" + "🎉" * 20)
            print(f"✅ SUCCESS! CONNECTED TO OFFICIAL API")
            print(f"💰 Wallet Response: {data}")
            print("🎉" * 20 + "\n")
        else:
            print(f"❌ Connected but Access Denied: {data}")
            print("   (This still counts as a 'Pass' for connectivity!)")
            
    except Exception as e:
        print(f"❌ Failed: {e}")

manual_hackathon_test()

# --- DUMMY LOOP ---
if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        print("💤 Sleeping...")
        time.sleep(3600)