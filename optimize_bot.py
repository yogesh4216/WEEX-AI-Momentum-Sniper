import pandas as pd
import pickle
import numpy as np

print("🚀 Starting Hyperparameter Tuning (Finding the Sweet Spot)...")

# 1. Load Data & Model
df = pd.read_csv("btc_advanced_features.csv")
with open("my_first_ai_model.pkl", "rb") as f:
    model = pickle.load(f)

features = ['RSI', 'ATR', 'Return_1h', 'Return_2h', 'Return_3h', 
            'Volume_Change', 'Dist_SMA50']

split_point = int(len(df) * 0.8)
test_data_original = df.iloc[split_point:].copy()

# Pre-calculate probabilities to speed up the loop
probs = model.predict_proba(test_data_original[features])[:, 1]
test_data_original['Confidence'] = probs

# 2. THE SETTINGS TO TEST
thresholds_to_test = [0.55, 0.60, 0.65, 0.70, 0.75]

results = []

print(f"{'THRESHOLD':<10} | {'TRADES':<10} | {'FINAL BALANCE':<15} | {'PROFIT':<10}")
print("-" * 55)

# 3. THE LOOP (Test each setting)
for threshold in thresholds_to_test:
    # Reset simulation variables for each loop
    test_data = test_data_original.copy()
    balance = 1000
    btc_held = 0
    in_position = False
    buy_price = 0 
    trade_fee = 0.001
    trades_count = 0
    
    STOP_LOSS_PCT = 0.02
    TAKE_PROFIT_PCT = 0.05
    
    for index, row in test_data.iterrows():
        price = row['Close']
        confidence = row['Confidence']
        
        # RISK MANAGEMENT
        if in_position:
            change = (price - buy_price) / buy_price
            if change <= -STOP_LOSS_PCT: # Stop Loss
                balance = (btc_held * price) * (1 - trade_fee)
                btc_held = 0
                in_position = False
                continue
            elif change >= TAKE_PROFIT_PCT: # Take Profit
                balance = (btc_held * price) * (1 - trade_fee)
                btc_held = 0
                in_position = False
                continue

        # ENTRY LOGIC (Using the current loop's threshold)
        if not in_position and confidence >= threshold:
            btc_bought = (balance / price) * (1 - trade_fee)
            btc_held = btc_bought
            buy_price = price
            balance = 0
            in_position = True
            trades_count += 1
            
        # EXIT LOGIC (Standardize at 0.50 for all tests)
        elif in_position and confidence < 0.50:
            balance = (btc_held * price) * (1 - trade_fee)
            btc_held = 0
            in_position = False

    # Final Calculation
    if in_position:
        balance = btc_held * test_data.iloc[-1]['Close']
        
    profit = balance - 1000
    print(f"{threshold:<10} | {trades_count:<10} | ${balance:<14.2f} | ${profit:<9.2f}")
    results.append((threshold, profit))

# 4. FIND THE WINNER
best_setting = max(results, key=lambda x: x[1])
print("-" * 55)
print(f"🏆 BEST SETTING: Confidence > {best_setting[0]}")
print(f"💰 POTENTIAL PROFIT: ${best_setting[1]:.2f}")