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
    if not secret_key: return ""
    message = timestamp + method + endpoint + body
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def manual_hackathon_test():
    print("\n🛠️  STARTING CONTRACT DOMAIN TEST...")
    
    if not api_key:
        print("⚠️  Missing Keys. Check Railway Variables.")
        return

    # --- THE CRITICAL FIX: Use the FUTURES Domain ---
    # Research confirms this is the main domain for the AI Hackathon
    base_url = "https://api-contract.weex.com"
    
    # This endpoint checks your Futures Wallet Assets
    endpoint = "/api/v1/account/assets"
    
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    body = ""
    signature = get_signature(timestamp, method, endpoint, body)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-WEEX-ACCESS-KEY": api_key,
        "X-WEEX-ACCESS-PASSPHRASE": passphrase,
        "X-WEEX-ACCESS-TIMESTAMP": timestamp,
        "X-WEEX-ACCESS-SIGN": signature
    }

    print(f"👉 Connecting to: {base_url}{endpoint}")

    try:
        # Timeout increased to 20s to handle slow handshakes
        response = requests.get(base_url + endpoint, headers=headers, timeout=20, verify=False)
        
        print(f"   🔹 Status Code: {response.status_code}")
        
        try:
            data = response.json()
            # Code '00000' is success, but 'success' msg also counts
            if data.get('code') == '00000' or data.get('msg') == 'success':
                print("\n" + "🎉" * 20)
                print(f"✅ SUCCESS! CONNECTED TO WEEX FUTURES")
                print(f"💰 Wallet Response: {data}")
                print("🎉" * 20 + "\n")
            else:
                # Even an error like "Invalid API Key" proves we CONNECTED to the server
                print(f"✅ Connected (Server replied): {data}")
        except:
            print(f"❌ Response was not JSON: {response.text[:200]}")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

manual_hackathon_test()

# --- DUMMY LOOP ---
if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        time.sleep(3600)