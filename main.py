import time
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import pickle
import numpy as np
import ccxt  # <--- NEW: The library that talks to WEEX
import os
from datetime import datetime

# --- CONFIGURATION ---
SYMBOL = "BTC/USDT"   # WEEX uses this format
YF_SYMBOL = "BTC-USD" # Yahoo uses this format
TIMEFRAME = "1h"
CONFIDENCE_THRESHOLD = 0.60
MODEL_FILE = "my_first_ai_model.pkl"
USDT_AMOUNT = 10      # How many dollars to bet per trade

# --- AUTHENTICATION (Loads from Railway Variables) ---
api_key = os.environ.get("WEEX_API_KEY")
secret_key = os.environ.get("WEEX_SECRET_KEY")
passphrase = os.environ.get("WEEX_PASSPHRASE")  # <--- NEW: Required for Hackathon Key

print("🚀 AI TRADING BOT INITIALIZING...")

# 1. CONNECT TO WEEX
if not api_key:
    print("⚠️  WARNING: No API Keys found. Running in Simulation Mode.")
    exchange = None
else:
    try:
        exchange = ccxt.weex({
            'apiKey': api_key,
            'secret': secret_key,
            'password': passphrase,  # <--- Critical for your new key
            'options': {'defaultType': 'swap'} # 'swap' = Futures
        })
        
        # --- THE API TEST (CRITICAL) ---
        # Fetching balance proves to WEEX you are connected.
        balance = exchange.fetch_balance()
        free_usdt = balance['USDT']['free']
        print(f"✅ API CONNECTED! Wallet Balance: ${free_usdt:.2f} USDT")
        
    except Exception as e:
        print(f"❌ API Connection Failed: {e}")
        exchange = None

# 2. LOAD THE BRAIN
try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    print("🧠 AI Model Loaded Successfully.")
except FileNotFoundError:
    print("❌ Error: Model file not found. Train the AI first!")
    exit()

def fetch_and_prepare_data():
    """
    Fetches live data and calculates indicators.
    """
    # Fetch from Yahoo for the AI analysis (Stable & Fast)
    df = yf.download(YF_SYMBOL, period="1mo", interval="1h", progress=False)
    
    # Clean Data
    if 'Price' in df.columns:
        df = df.iloc[2:]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Ensure numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate Features
    df['RSI'] = df.ta.rsi(length=14)
    df['SMA_50'] = df.ta.sma(length=50)
    df['ATR'] = df.ta.atr(length=14)
    df['Return_1h'] = df['Close'].pct_change(periods=1)
    df['Return_2h'] = df['Close'].pct_change(periods=2)
    df['Return_3h'] = df['Close'].pct_change(periods=3)
    df['Volume'] = df['Volume'].replace(0, 0.001)
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Dist_SMA50'] = (df['Close'] - df['SMA_50']) / df['SMA_50']
    
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.dropna(inplace=True)
    return df

def execute_trade(side):
    """
    Actually places the order on WEEX.
    """
    if exchange is None:
        print("⚠️  Simulation Mode: Trade skipped (No API).")
        return

    try:
        # Check Balance First
        balance = exchange.fetch_balance()
        usdt_free = balance['USDT']['free']

        if usdt_free < USDT_AMOUNT:
            print(f"❌ Insufficient Funds (${usdt_free:.2f}). Needs ${USDT_AMOUNT}.")
            return

        # Execute Market Order
        print(f"⚡ EXECUTING REAL {side.upper()} ORDER for ${USDT_AMOUNT}...")
        order = exchange.create_market_order(SYMBOL, side, amount=None, price=None, params={'cost': USDT_AMOUNT})
        print(f"✅ Trade Successful! Order ID: {order['id']}")
        
    except Exception as e:
        print(f"❌ Trade Failed: {e}")

def run_bot():
    print(f"\n📡 Connecting to Market ({YF_SYMBOL})...")
    
    # Get latest data
    df = fetch_and_prepare_data()
    latest = df.iloc[-1]
    
    # Prepare input
    features = ['RSI', 'ATR', 'Return_1h', 'Return_2h', 'Return_3h', 
                'Volume_Change', 'Dist_SMA50']
    input_data = pd.DataFrame([latest[features]])
    
    # Ask AI
    prediction_prob = model.predict_proba(input_data)[0][1] 
    
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"💵 Price: ${latest['Close']:.2f}")
    print(f"📊 RSI: {latest['RSI']:.2f}")
    print(f"🤖 Confidence: {prediction_prob*100:.2f}%")
    
    # Decision
    if prediction_prob >= CONFIDENCE_THRESHOLD:
        print("✅ SIGNAL: STRONG BUY!")
        execute_trade('buy')
    else:
        print("⏸️  SIGNAL: HOLD.")

if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        try:
            run_bot()
            print("💤 Sleeping for 60 minutes...")
            time.sleep(3600)
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)