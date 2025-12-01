import requests

# We are using CoinGecko just to practice. 
# It works almost exactly like WEEX but is easier to access.
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usdt"

print(f"🚀 Connecting to CoinGecko (Backup Plan)...")

try:
    response = requests.get(url)
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("🎉 SUCCESS! We got data:")
        print(f"💰 Bitcoin Price: ${data['bitcoin']['usdt']}")
        print(f"💰 Ethereum Price: ${data['ethereum']['usdt']}")
        print("\n(Now you know your Python works! The issue is definitely the WEEX block.)")
    else:
        print(f"❌ Error: {response.status_code}")

except Exception as e:
    print(f"❌ Crash: {e}")