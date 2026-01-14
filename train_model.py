import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

print("\n==============================")
print(" MODEL TRAINING STARTED ⏳")
print("==============================\n")

# Load data
df = pd.read_csv("data.csv")

if df.empty:
    print("❌ No data available to train.")
    exit()

df['time_index'] = range(len(df))

X = df[['time_index']]
y = df['temperature']

model = LinearRegression()

model.fit(X, y)

print("✅ Model Training Completed!")
print("Saving model...")

joblib.dump(model, "temperature_model.pkl")

print("🎉 Model saved as temperature_model.pkl")
print("You can now run predict.py")
print("\n==============================\n")
