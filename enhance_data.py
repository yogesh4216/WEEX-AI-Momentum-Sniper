import pandas as pd
import pandas_ta as ta
import numpy as np

print("🚀 Upgrading Data with 'Memory' (FIXED VERSION)...")

# 1. Load the RAW data
df = pd.read_csv("btc_training_data.csv")

# Clean formatting
if 'Price' in df.columns:
    df = df.iloc[2:]
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df = df.reset_index(drop=True)

cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 2. Add Basic Indicators
df['RSI'] = df.ta.rsi(length=14)
df['SMA_50'] = df.ta.sma(length=50)
df['ATR'] = df.ta.atr(length=14)

# 3. Add "Lag" Features (Memory)
df['Return_1h'] = df['Close'].pct_change(periods=1)
df['Return_2h'] = df['Close'].pct_change(periods=2)
df['Return_3h'] = df['Close'].pct_change(periods=3)

# Handle Volume: Replace 0 with a tiny number to avoid "divide by zero" errors
df['Volume'] = df['Volume'].replace(0, 0.001)
df['Volume_Change'] = df['Volume'].pct_change()

# 4. Add "Context"
df['Dist_SMA50'] = (df['Close'] - df['SMA_50']) / df['SMA_50']

# 5. Define Target (Predict if price goes UP > 0.2%)
future_return = df['Close'].shift(-1) / df['Close'] - 1
df['Target'] = (future_return > 0.002).astype(int) 

# --- THE FIX IS HERE ---
# 6. Clean Infinite Values (The "Janitor")
print("🧹 Cleaning up infinite values...")
df.replace([np.inf, -np.inf], 0, inplace=True)
df.dropna(inplace=True)
# -----------------------

output_file = "btc_advanced_features.csv"
df.to_csv(output_file, index=False)

print(f"✅ Data Fixed & Saved to {output_file}")
print(f"Rows ready for training: {len(df)}")