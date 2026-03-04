import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ----------------------------
# 1. Load Dataset
# ----------------------------
df = pd.read_csv("dataset/flowpay_water_usage_iso.csv")

# ----------------------------
# 2. Convert ISO Timestamp to Datetime
# ----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ----------------------------
# 3. Create Numeric Day Feature
# ----------------------------
df["day_number"] = (df["timestamp"] - df["timestamp"].min()).dt.days

# ----------------------------
# 4. Prepare Data for Regression
# ----------------------------
X = df[["day_number"]]
y = df["water_consumed_liters"]

# ----------------------------
# 5. Train Linear Regression Model
# ----------------------------
model = LinearRegression()
model.fit(X, y)

# ----------------------------
# 6. Predict Next Day Usage
# ----------------------------
next_day_number = df["day_number"].max() + 1
prediction = model.predict(pd.DataFrame([[next_day_number]], columns=['day_number']))

print("Predicted water usage for next day:", round(prediction[0], 2), "liters")

# ----------------------------
# 7. Simulate Actual Usage & Detect Anomaly
# ----------------------------
actual_usage = 300  # simulate abnormal spike

print("Actual usage:", actual_usage, "liters")

if actual_usage > prediction[0] * 1.5:
    print("Anomaly detected: Possible leak or abnormal consumption.")
else:
    print("Usage is within expected range.")

# ----------------------------
# 8. Plot Results
# ----------------------------
plt.scatter(df["day_number"], y)
plt.plot(df["day_number"], model.predict(X))
plt.xlabel("Day Number")
plt.ylabel("Water Consumed (Liters)")
plt.title("Water Usage Prediction using Linear Regression")
plt.show()