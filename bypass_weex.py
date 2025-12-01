import cloudscraper
import json

print("🚀 Launching Cloudscraper (Bypassing Bot Protection)...")

# 1. Create a scraper instance (This acts like Chrome)
scraper = cloudscraper.create_scraper()

# 2. Define the URL
url = "https://api-spot.weex.com/api/v2/public/products"

try:
    print(f"📡 Connecting to {url}...")
    
    # 3. Request data using the scraper instead of 'requests'
    response = scraper.get(url)

    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('data', [])
        print(f"🎉 SUCCESS! Found {len(products)} trading pairs.")
        
        # Print the first pair to prove we have real data
        if products:
            print(f"🥇 First Pair: {products[0]['symbol']}")
    else:
        print(f"❌ Failed. Server Message: {response.text}")

except Exception as e:
    print(f"❌ Crash: {e}")