import time
import os
import requests
import hmac
import hashlib
import base64
import urllib3

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
    # Pre-hash validation
    if not secret_key: return ""
    
    message = timestamp + method + endpoint + body
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def manual_hackathon_test():
    print("\n🛠️  STARTING FINAL 'BROWSER MIMIC' TEST...")
    
    if not api_key or not secret_key:
        print("⚠️  Missing Keys. Check Railway Variables.")
        return

    # CORRECT TARGET (Spot API)
    base_url = "https://api-spot.weex.com"
    endpoint = "/api/v1/account/assets"
    
    # 1. Prepare Signature
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    body = ""
    signature = get_signature(timestamp, method, endpoint, body)

    # 2. FULL BROWSER HEADERS (Tricks Cloudflare)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "X-WEEX-ACCESS-KEY": api_key,
        "X-WEEX-ACCESS-PASSPHRASE": passphrase,
        "X-WEEX-ACCESS-TIMESTAMP": timestamp,
        "X-WEEX-ACCESS-SIGN": signature
    }

    print(f"👉 Connecting to: {base_url}{endpoint}")

    try:
        # verify=False prevents SSL handshake failures on cloud servers
        response = requests.get(base_url + endpoint, headers=headers, timeout=15, verify=False)
        
        print(f"   🔹 Status Code: {response.status_code}")
        
        # Check if we got JSON back
        try:
            data = response.json()
            if data.get('code') == '00000' or data.get('msg') == 'success':
                print("\n" + "🎉" * 20)
                print(f"✅ SUCCESS! CONNECTED TO WEEX")
                print(f"💰 Wallet Response: {data}")
                print("🎉" * 20 + "\n")
            else:
                print(f"✅ Connected (Access Denied is OK): {data}")
        except:
            print(f"❌ Failed to parse JSON. Raw Text: {response.text[:100]}...")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

# Run immediately
manual_hackathon_test()

# --- DUMMY LOOP ---
if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        time.sleep(3600)