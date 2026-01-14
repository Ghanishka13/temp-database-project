import pandas as pd
import joblib
from datetime import timedelta

DATA_FILE = "data.csv"

try:
    df = pd.read_csv(DATA_FILE)
except:
    print("❌ data.csv not found. Run server first.")
    exit()

if df.empty:
    print("❌ No data found.")
    exit()

# Load model
try:
    model = joblib.load("temperature_model.pkl")
except:
    print("❌ Model not trained! Run train_model.py first.")
    exit()

# Prediction time (in minutes)
predict_minutes_ahead = 10  # change if needed
interval_seconds = 10  # ESP32 sends every 10 sec
predict_index = len(df) + (predict_minutes_ahead * 60) // interval_seconds

predicted_temp = model.predict([[predict_index]])[0]

# Calculate future time
last_time = pd.to_datetime(df["timestamp"].iloc[-1])
future_time = last_time + timedelta(minutes=predict_minutes_ahead)

print("\n==============================")
print("  FUTURE TEMPERATURE PREDICTION")
print("==============================\n")
print(f"Last Recorded Time: {last_time}")
print(f"Predicting {predict_minutes_ahead} minutes ahead...")
print(f"\n🌡️ Predicted Temperature at {future_time}: {predicted_temp:.2f} °C")
print("\n==============================\n")
