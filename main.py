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
    print("\n🛠️  STARTING FORENSIC CONNECTION TEST...")
    
    if not api_key:
        print("⚠️  Missing Keys. Skipping.")
        return

    # LIST OF TARGETS TO TRY
    # We will try both the main domain (with a header hack) and the spot domain
    targets = [
        ("https://api.weex.com", "/api/v1/account/assets"),
        ("https://api-spot.weex.com", "/api/v1/account/assets")
    ]

    for base_url, endpoint in targets:
        print(f"\n👉 Testing Target: {base_url} ...")
        
        method = "GET"
        body = ""
        timestamp = str(int(time.time() * 1000))
        signature = get_signature(timestamp, method, endpoint, body)

        # HEADERS (Now with User-Agent to prevent 403 Blocks)
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-WEEX-ACCESS-KEY": api_key,
            "X-WEEX-ACCESS-PASSPHRASE": passphrase,
            "X-WEEX-ACCESS-TIMESTAMP": timestamp,
            "X-WEEX-ACCESS-SIGN": signature
        }

        try:
            # We use verify=False to avoid SSL headaches on Railway
            response = requests.get(base_url + endpoint, headers=headers, timeout=10, verify=False)
            
            # DEBUG PRINT (Critical)
            print(f"   🔹 Status Code: {response.status_code}")
            
            try:
                data = response.json()
                if data.get('code') == '00000' or data.get('msg') == 'success':
                    print("\n" + "🎉" * 20)
                    print(f"✅ SUCCESS! Connected to {base_url}")
                    print(f"💰 Wallet Response: {data}")
                    print("🎉" * 20 + "\n")
                    return # Stop on success
                else:
                    print(f"   ❌ Access Denied (But Connected!): {data}")
            except json.JSONDecodeError:
                # THIS IS WHERE WE CATCH THE ERROR YOU SAW
                print(f"   ❌ RESPONSE WAS NOT JSON! RAW OUTPUT:")
                print(f"   {response.text[:200]}") # Print first 200 chars to see if it's HTML
                
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")

manual_hackathon_test()

# --- DUMMY LOOP ---
if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        print("💤 Sleeping...")
        time.sleep(3600)