import time
import pickle
import os
import requests
import hmac
import hashlib
import base64
import json
from datetime import datetime

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
    print("\n🛠️  STARTING MULTI-DOMAIN CONNECTION TEST...")
    
    if not api_key or not secret_key:
        print("⚠️  Missing Keys. Skipping Test.")
        return

    # LIST OF POTENTIAL DOMAINS TO HUNT
    domains = [
        "https://api.weex.com",
        "https://api.weex.vip",     # Alternative 1
        "https://api.weex.io",      # Alternative 2
        "https://api.weex.com"      # Alternative 3
    ]
    
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

    # 1. CHECK INTERNET FIRST
    try:
        requests.get("https://google.com", timeout=5)
        print("✅ Internet Connection: OK")
    except:
        print("❌ CRITICAL: Railway server has NO Internet access!")

    # 2. HUNT FOR THE WORKING DOMAIN
    for base_url in domains:
        print(f"👉 Trying: {base_url} ...")
        try:
            url = base_url + endpoint
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            if data.get('code') == '00000' or data.get('msg') == 'success':
                print("\n" + "✅" * 20)
                print(f"🎉 SUCCESS! Connected via: {base_url}")
                print(f"💰 Wallet Response: {data}")
                print("✅" * 20 + "\n")
                return # Stop after success
            else:
                print(f"   ❌ Connected but Access Denied: {data}")
                # If access denied, at least we connected! That counts as a pass.
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")

manual_hackathon_test()

# --- DUMMY LOOP ---
if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        print("💤 Sleeping (Test Complete)...")
        time.sleep(3600)