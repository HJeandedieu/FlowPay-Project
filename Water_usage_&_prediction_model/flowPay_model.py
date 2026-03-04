import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("dataset/flowpay_water_usage_iso.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["day_number"] = (df["timestamp"] - df["timestamp"].min()).dt.days

# Prepare data for Linear Regression

X = df[["day_number"]]
y = df["water_consumed_liters"]


# Train Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# 6. Predict Next Day Usage
next_day_number = df["day_number"].max() + 1
prediction = model.predict(pd.DataFrame([[next_day_number]], columns=['day_number']))

print("Predicted water usage for next day:", round(prediction[0], 2), "liters")


# 7. Simulate Actual Usage & Detect Anomaly
actual_usage = 300  # simulate abnormal spike

print("Actual usage:", actual_usage, "liters")

if actual_usage > prediction[0] * 1.5:
    print("Anomaly detected: Possible leak or abnormal consumption.")
else:
    print("Usage is within expected range.")


# 8. Plot Results
plt.scatter(df["day_number"], y)
plt.plot(df["day_number"], model.predict(X))
plt.xlabel("Day Number")
plt.ylabel("Water Consumed (Liters)")
plt.title("Water Usage Prediction using Linear Regression")
plt.show()