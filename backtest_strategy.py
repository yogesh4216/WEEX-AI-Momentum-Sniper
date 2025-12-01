import pandas as pd
import pickle

print("🚀 Starting SNIPER MODE Backtest...")

# 1. Load Data & Model
df = pd.read_csv("btc_advanced_features.csv")
with open("my_first_ai_model.pkl", "rb") as f:
    model = pickle.load(f)

features = ['RSI', 'ATR', 'Return_1h', 'Return_2h', 'Return_3h', 
            'Volume_Change', 'Dist_SMA50']

split_point = int(len(df) * 0.8)
test_data = df.iloc[split_point:].copy()

# 2. GET CONFIDENCE SCORES (The Sniper Scope)
# predict_proba returns pairs: [Prob of 0, Prob of 1]
# We only want the second number (Probability of Buy)
probs = model.predict_proba(test_data[features])[:, 1]
test_data['Confidence'] = probs

# 3. TRADING LOOP
balance = 1000
btc_held = 0
in_position = False
buy_price = 0 
trade_fee = 0.001

# --- SETTINGS ---
CONFIDENCE_THRESHOLD = 0.65  # Only buy if AI is 65% sure (Sniper Mode)
STOP_LOSS_PCT = 0.02         # 2% Safety Net
TAKE_PROFIT_PCT = 0.05       # 5% Target
# ----------------

print(f"\n💰 Initial Balance: ${balance}")
trades_count = 0

for index, row in test_data.iterrows():
    price = row['Close']
    confidence = row['Confidence']
    
    # 1. RISK MANAGEMENT (Always check first)
    if in_position:
        change = (price - buy_price) / buy_price
        
        if change <= -STOP_LOSS_PCT:
            new_balance = (btc_held * price) * (1 - trade_fee)
            balance = new_balance
            btc_held = 0
            in_position = False
            print(f"🛑 STOP LOSS at ${price:.2f} | Loss: {change*100:.2f}% | Bal: ${balance:.2f}")
            continue

        elif change >= TAKE_PROFIT_PCT:
            new_balance = (btc_held * price) * (1 - trade_fee)
            balance = new_balance
            btc_held = 0
            in_position = False
            print(f"💰 TAKE PROFIT at ${price:.2f} | Gain: {change*100:.2f}% | Bal: ${balance:.2f}")
            continue

    # 2. SNIPER ENTRY LOGIC
    # Only buy if we are NOT in position AND confidence is high
    if not in_position and confidence >= CONFIDENCE_THRESHOLD:
        btc_bought = (balance / price) * (1 - trade_fee)
        btc_held = btc_bought
        buy_price = price
        balance = 0
        in_position = True
        trades_count += 1
        print(f"🟢 SNIPER BUY at ${price:.2f} | Confidence: {confidence*100:.1f}%")
        
    # 3. EXIT LOGIC
    # Sell if confidence drops below 50% (The AI changed its mind)
    elif in_position and confidence < 0.50:
        new_balance = (btc_held * price) * (1 - trade_fee)
        balance = new_balance
        btc_held = 0
        in_position = False
        print(f"👋 AI EXIT at ${price:.2f} | Bal: ${balance:.2f}")

# Final Tally
if in_position:
    balance = btc_held * test_data.iloc[-1]['Close']

print("------------------------------------------------")
print(f"🏁 Final Balance: ${balance:.2f}")
print(f"📊 Total Trades: {trades_count}")
print(f"📈 Total Profit/Loss: ${balance - 1000:.2f}")