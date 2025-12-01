import time
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import pickle
import numpy as np
from datetime import datetime

# --- CONFIGURATION ---
SYMBOL = "BTC-USD"
TIMEFRAME = "1h"
CONFIDENCE_THRESHOLD = 0.60  # The "Strategic Choice" for Hackathon
MODEL_FILE = "my_first_ai_model.pkl"

print("🚀 AI TRADING BOT INITIALIZING...")
print(f"🎯 Strategy: Random Forest | Threshold: {CONFIDENCE_THRESHOLD}")

# 1. LOAD THE BRAIN
try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    print("🧠 AI Model Loaded Successfully.")
except FileNotFoundError:
    print("❌ Error: Model file not found. Train the AI first!")
    exit()

def fetch_and_prepare_data():
    """
    Fetches live data and calculates the technical indicators
    exactly how the AI learned them.
    """
    # 1. Get Data (Using Yahoo for Demo/Reliability)
    # We fetch 500 hours to ensure Moving Averages are accurate
    df = yf.download(SYMBOL, period="1mo", interval=TIMEFRAME, progress=False)
    
    # Clean Data
    if 'Price' in df.columns:
        df = df.iloc[2:]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Ensure numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Calculate Indicators (The "Features")
    df['RSI'] = df.ta.rsi(length=14)
    df['SMA_50'] = df.ta.sma(length=50)
    df['ATR'] = df.ta.atr(length=14)
    
    # Lag Features (Memory)
    df['Return_1h'] = df['Close'].pct_change(periods=1)
    df['Return_2h'] = df['Close'].pct_change(periods=2)
    df['Return_3h'] = df['Close'].pct_change(periods=3)
    
    # Volume & Context
    df['Volume'] = df['Volume'].replace(0, 0.001)
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Dist_SMA50'] = (df['Close'] - df['SMA_50']) / df['SMA_50']
    
    # Clean Infinites
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.dropna(inplace=True)
    
    return df

def run_bot():
    """
    The Main Loop: Checks market, asks AI, decides to trade.
    """
    print(f"\n📡 Connecting to Market ({SYMBOL})...")
    
    # Get the very latest data
    df = fetch_and_prepare_data()
    latest = df.iloc[-1] # The most recent hour
    
    # Prepare the input for the AI
    features = ['RSI', 'ATR', 'Return_1h', 'Return_2h', 'Return_3h', 
                'Volume_Change', 'Dist_SMA50']
    
    # Reshape for the model (it expects a list of rows)
    input_data = pd.DataFrame([latest[features]])
    
    # ASK THE AI
    # [0] is Prob of Down, [1] is Prob of Up
    prediction_prob = model.predict_proba(input_data)[0][1] 
    
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"💵 Current Price: ${latest['Close']:.2f}")
    print(f"📊 RSI: {latest['RSI']:.2f}")
    print(f"🤖 AI Confidence (BUY): {prediction_prob*100:.2f}%")
    
    # DECISION LOGIC
    if prediction_prob >= CONFIDENCE_THRESHOLD:
        print("✅ SIGNAL: STRONG BUY! Executing Trade...")
        # In the real competition, you would add:
        # weex_api.place_order(symbol="BTC", side="BUY", amount=...)
    else:
        print("⏸️  SIGNAL: HOLD. Waiting for better opportunity.")

# Run once to show it works
if __name__ == "__main__":
    run_bot()