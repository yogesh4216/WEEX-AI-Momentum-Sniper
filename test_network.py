import requests

def check_site(url, name):
    print(f"Testing connection to {name}...")
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ {name} is ALIVE! (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ {name} is BLOCKED or DOWN. Error: {e}")

# 1. Test Google (To prove your internet works)
check_site("https://www.google.com", "Google")

# 2. Test WEEX (To prove it's being blocked)
check_site("https://api-spot.weex.com/api/v2/public/products", "WEEX")