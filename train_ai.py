import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle # <--- We need this to save!

print("🚀 Starting Advanced Training Session...")

# 1. Load the NEW Advanced Data
df = pd.read_csv("btc_advanced_features.csv")

# 2. Define the New Feature Set
features = ['RSI', 'ATR', 'Return_1h', 'Return_2h', 'Return_3h', 
            'Volume_Change', 'Dist_SMA50']

X = df[features]
y = df['Target']

# 3. Split (80/20)
split_point = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_point], X.iloc[split_point:]
y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]

# 4. Train
print("🧠 Training the brain...")
model = RandomForestClassifier(n_estimators=200, min_samples_split=20, random_state=42)
model.fit(X_train, y_train)

# 5. Test
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"🎯 New Accuracy Score: {accuracy * 100:.2f}%")
print("------------------------------------------------")
print(classification_report(y_test, predictions))

# --- THE MISSING PART IS BELOW ---

# 6. SAVE THE MODEL (Crucial Step)
filename = "my_first_ai_model.pkl"
with open(filename, "wb") as f:
    pickle.dump(model, f)
print(f"💾 SUCCESS: Model saved to {filename}")

# 7. Feature Importance
print("\n🧠 Feature Importance:")
for name, score in zip(features, model.feature_importances_):
    print(f"{name}: {score:.4f}")