import yfinance as yf
import pandas as pd

print("🚀 Starting Data Harvester...")

# 1. Define the symbol (Yahoo uses 'BTC-USD' instead of 'BTCUSDT')
symbol = "BTC-USD"

# 2. Download 1 year of data with 1-hour intervals
# (This is perfect for training a trading bot)
print(f"📥 Downloading data for {symbol}...")
data = yf.download(symbol, period="1y", interval="1h")

# 3. Check if we got data
if not data.empty:
    print(f"✅ Success! Downloaded {len(data)} rows of data.")
    
    # 4. Preview the data
    print("\n📊 First 5 rows:")
    print(data.head())
    
    # 5. Save to CSV (Excel format) so we can use it for AI training
    filename = "btc_training_data.csv"
    data.to_csv(filename)
    print(f"\n💾 Saved to {filename}. You are ready for Phase 2!")
    
else:
    print("❌ Error: No data found. Check your internet.")