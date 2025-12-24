import time
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import pickle
import numpy as np
import ccxt
import os
import sys
from datetime import datetime

# --- CONFIGURATION ---
SYMBOL = "BTC/USDT"
YF_SYMBOL = "BTC-USD"
TIMEFRAME = "1h"
CONFIDENCE_THRESHOLD = 0.60
MODEL_FILE = "my_first_ai_model.pkl"
USDT_AMOUNT = 10

# --- AUTHENTICATION ---
api_key = os.environ.get("WEEX_API_KEY")
secret_key = os.environ.get("WEEX_SECRET_KEY")
passphrase = os.environ.get("WEEX_PASSPHRASE")

print("🚀 AI TRADING BOT INITIALIZING...")

# --- DEBUGGING THE VERSION ERROR ---
print(f"🔍 DEBUG INFO:")
print(f"   • Python Version: {sys.version}")
print(f"   • CCXT Version: {ccxt.__version__}")
print(f"   • Is 'weex' in exchanges list? {'weex' in ccxt.exchanges}")

# 1. CONNECT TO WEEX (With Fallback Method)
exchange = None
if not api_key:
    print("⚠️  WARNING: No API Keys found. Running in Simulation Mode.")
else:
    try:
        # METHOD A: Direct (Standard)
        if hasattr(ccxt, 'weex'):
            print("✅ Found 'weex' attribute directly.")
            exchange_class = ccxt.weex
        else:
            # METHOD B: Dynamic (Fixes attribute errors)
            print("⚠️ 'weex' attribute missing. Trying dynamic load...")
            exchange_class = getattr(ccxt, 'weex')

        exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret_key,
            'password': passphrase,
            'options': {'defaultType': 'swap'}
        })
        
        # TEST CONNECTION
        balance = exchange.fetch_balance()
        free_usdt = balance['USDT']['free']
        print(f"✅ API CONNECTED! Wallet Balance: ${free_usdt:.2f} USDT")
        
    except AttributeError:
        print("❌ CRITICAL ERROR: Your CCXT library is definitely too old.")
        print("   -> Railway is ignoring the update. We may need to redeploy without cache.")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

# 2. LOAD THE BRAIN
try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    print("🧠 AI Model Loaded Successfully.")
except FileNotFoundError:
    print("❌ Error: Model file not found.")
    exit()

def fetch_and_prepare_data():
    df = yf.download(YF_SYMBOL, period="1mo", interval="1h", progress=False)
    if 'Price' in df.columns:
        df = df.iloc[2:]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
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
    if exchange is None:
        return
    try:
        balance = exchange.fetch_balance()
        if balance['USDT']['free'] < USDT_AMOUNT:
            print("❌ Insufficient Funds.")
            return
        print(f"⚡ EXECUTING {side.upper()}...")
        exchange.create_market_order(SYMBOL, side, amount=None, price=None, params={'cost': USDT_AMOUNT})
        print("✅ Trade Executed!")
    except Exception as e:
        print(f"❌ Trade Failed: {e}")

def run_bot():
    print(f"\n📡 Connecting to Market ({YF_SYMBOL})...")
    try:
        df = fetch_and_prepare_data()
        latest = df.iloc[-1]
        features = ['RSI', 'ATR', 'Return_1h', 'Return_2h', 'Return_3h', 'Volume_Change', 'Dist_SMA50']
        input_data = pd.DataFrame([latest[features]])
        prediction_prob = model.predict_proba(input_data)[0][1] 
        
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"💵 Price: ${latest['Close']:.2f}")
        print(f"📊 RSI: {latest['RSI']:.2f}")
        print(f"🤖 Confidence: {prediction_prob*100:.2f}%")
        
        if prediction_prob >= CONFIDENCE_THRESHOLD:
            print("✅ SIGNAL: BUY!")
            execute_trade('buy')
        else:
            print("⏸️  SIGNAL: HOLD.")
            
    except Exception as e:
        print(f"❌ Error in loop: {e}")

if __name__ == "__main__":
    print("🔄 Bot started. Press Ctrl+C to stop.")
    while True:
        run_bot()
        print("💤 Sleeping for 60 minutes...")
        time.sleep(3600)