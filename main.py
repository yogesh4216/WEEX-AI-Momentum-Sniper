import time
import pickle
import numpy as np
import os
import sys
import requests
import hmac
import hashlib
import base64
import json
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- CONFIGURATION ---
MODEL_FILE = "my_first_ai_model.pkl"
SYMBOL = "BTC/USDT"
YF_SYMBOL = "BTC-USD"

# --- AUTHENTICATION ---
api_key = os.environ.get("WEEX_API_KEY")
secret_key = os.environ.get("WEEX_SECRET_KEY")
passphrase = os.environ.get("WEEX_PASSPHRASE")

print("🚀 AI TRADING BOT INITIALIZING...")

# --- 1. THE MANUAL BYPASS TEST (Guaranteed to work) ---
def manual_hackathon_test():
    print("🛠️  Starting Manual Connection Test...")
    
    if not api_key or not secret_key:
        print("⚠️  Missing Keys. Skipping Test.")
        return

    # WEEX API Details
    base_url = "https://api.weex.com"
    endpoint = "/api/v1/account/assets" 
    
    # 1. Prepare Signature
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    body = ""
    
    # Signature String
    message = timestamp + method + endpoint + body
    
    # Sign with HMAC SHA256
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
    # 2. Prepare Headers
    headers = {
        "Content-Type": "application/json",
        "X-WEEX-ACCESS-KEY": api_key,
        "X-WEEX-ACCESS-PASSPHRASE": passphrase,
        "X-WEEX-ACCESS-TIMESTAMP": timestamp,
        "X-WEEX-ACCESS-SIGN": signature_b64
    }
    
    # 3. Send Request
    try:
        print("📨 Sending request to WEEX...")
        response = requests.get(base_url + endpoint, headers=headers)
        data = response.json()
        
        # Check for Success codes
        if data.get('code') == '00000' or data.get('msg') == 'success':
            print("\n" + "="*40)
            print(f"✅ API CONNECTED! (Manual Bypass Successful)")
            print(f"💰 Wallet Response: {data}") 
            print("="*40 + "\n")
        else:
            print(f"❌ Connection Refused: {data}")
            
    except Exception as e:
        print(f"❌ Manual Test Failed: {e}")

# RUN THE TEST IMMEDIATELY ON STARTUP
manual_hackathon_test()

# --- 2. DUMMY BOT LOOP (Keeps Railway Alive) ---
try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    print("🧠 AI Model Loaded Successfully.")
except:
    print("⚠️ Model not found (Ignore this for now).")

if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        print(f"💤 Bot is sleeping (Test Completed)... {datetime.now()}")
        time.sleep(3600)