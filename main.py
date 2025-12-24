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

# Disable SSL warnings for the IP connection hack
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

def resolve_ip_manually():
    """
    Asks Google DNS for the real IP address of WEEX
    """
    print("🔎 Asking Google DNS for WEEX IP...")
    try:
        # Use Google's Public DNS API
        url = "https://dns.google/resolve?name=api.weex.com"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        
        if 'Answer' in data:
            # Get the first IP address found
            real_ip = data['Answer'][0]['data']
            print(f"✅ FOUND IP: {real_ip}")
            return real_ip
    except Exception as e:
        print(f"❌ DNS Lookup Failed: {e}")
    
    return None

def manual_hackathon_test():
    print("\n🛠️  STARTING DNS-BYPASS CONNECTION TEST...")
    
    if not api_key:
        print("⚠️  Missing Keys. Skipping.")
        return

    # 1. GET THE IP MANUALLY
    target_ip = resolve_ip_manually()
    
    if not target_ip:
        print("❌ Could not resolve IP. Retrying default domain...")
        base_url = "https://api.weex.com"
    else:
        # Construct URL using the IP directly
        base_url = f"https://{target_ip}"
        print(f"👉 Connecting directly to IP: {base_url}")

    endpoint = "/api/v1/account/assets"
    method = "GET"
    body = ""
    timestamp = str(int(time.time() * 1000))
    signature = get_signature(timestamp, method, endpoint, body)

    # 2. PREPARE HEADERS (Host is CRITICAL here)
    headers = {
        "Content-Type": "application/json",
        "X-WEEX-ACCESS-KEY": api_key,
        "X-WEEX-ACCESS-PASSPHRASE": passphrase,
        "X-WEEX-ACCESS-TIMESTAMP": timestamp,
        "X-WEEX-ACCESS-SIGN": signature,
        "Host": "api.weex.com"  # <--- Tells the server who we want to talk to
    }

    # 3. CONNECT
    try:
        # verify=False is needed because the SSL cert matches the Domain, not the IP.
        # This is safe for a test script.
        response = requests.get(base_url + endpoint, headers=headers, timeout=10, verify=False)
        data = response.json()
        
        if data.get('code') == '00000' or data.get('msg') == 'success':
            print("\n" + "🎉" * 20)
            print(f"✅ SUCCESS! CONNECTED VIA IP BYPASS")
            print(f"💰 Wallet Response: {data}")
            print("🎉" * 20 + "\n")
        else:
            print(f"❌ Connected but Access Denied: {data}")
            
    except Exception as e:
        print(f"❌ Failed: {e}")

manual_hackathon_test()

# --- DUMMY LOOP ---
if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        print("💤 Sleeping...")
        time.sleep(3600)