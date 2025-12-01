import requests

print("🚀 Script starting... (Stealth Mode)")

# 1. Define the URL 
# We are switching to the SPOT API first, it's usually friendlier.
url = "https://api-spot.weex.com/api/v2/public/products"

# 2. THE DISGUISE (Headers)
# This tells the server: "I am not a script, I am a Chrome Browser on a Mac"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

try:
    print(f"📡 Connecting to {url}...")
    
    # 3. Send the request WITH headers
    response = requests.get(url, headers=headers, timeout=10)

    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('data', [])
        print(f"🎉 SUCCESS! The door opened.")
        print(f"📊 Found {len(products)} trading pairs.")
        
        # Print the first one to prove it works
        if products:
            first_pair = products[0]
            print(f"🥇 Sample: {first_pair.get('symbol')} | Price: {first_pair.get('open')}")
    else:
        # If it fails again, print the raw text to see WHY
        print(f"❌ Blocked again. Server said: {response.text[:200]}")

except Exception as e:
    print(f"❌ Crash: {e}")