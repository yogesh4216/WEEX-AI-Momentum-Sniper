import pandas as pd
import pandas_ta as ta

print("🚀 Starting Feature Engineering...")

# 1. Load your raw data
df = pd.read_csv("btc_training_data.csv")

# Clean up column names (Yahoo sometimes adds extra rows/headers)
# We ensure the columns are clean: 'Open', 'High', 'Low', 'Close', 'Volume'
# Depending on how yfinance saved it, we might need to fix headers.
# This logic auto-detects standard yfinance format.
if 'Price' in df.columns:
    df = df.iloc[2:] # Skip the weird multi-level headers from yfinance
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df = df.reset_index(drop=True)

# Ensure numeric values
cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print("📊 Calculating Indicators (Giving the AI eyes)...")

# 2. Add RSI (Relative Strength Index)
# Strategy: If RSI < 30 (Oversold) -> Buy Signal?
df['RSI'] = df.ta.rsi(length=14)

# 3. Add Moving Averages (Trend)
# SMA 50: Short term trend
# SMA 200: Long term trend
df['SMA_50'] = df.ta.sma(length=50)
df['SMA_200'] = df.ta.sma(length=200)

# 4. Create the "Target" (What we want the AI to learn)
# We want to predict: "Will price go UP in the next hour?"
# Logic: If Close price next hour > Close price now, Target = 1. Else 0.
df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# 5. Clean Data (Remove empty rows created by calculations)
# (SMA_200 needs 200 rows of history to start working, so the first 200 rows are empty)
df.dropna(inplace=True)

# 6. Save the upgraded data
output_file = "btc_ready_for_ai.csv"
df.to_csv(output_file, index=False)

print(f"✅ Success! Feature engineering complete.")
print(f"💾 Saved to {output_file}. Rows: {len(df)}")
print("\nPreview of what the AI sees:")
print(df[['Date', 'Close', 'RSI', 'SMA_50', 'Target']].head())