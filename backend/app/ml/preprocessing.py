import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

data = pd.read_csv("sensor_data.csv")

data.columns = data.columns.str.strip().str.lower()
data["measurement"] = data["measurement"].str.strip().str.lower()

data["timestamp"] = pd.to_datetime(data["timestamp"])
data["timestamp"] = data["timestamp"].dt.floor("s")

data = data.groupby(["timestamp", "measurement"])["value"].mean().reset_index()

df = data.pivot(index="timestamp", columns="measurement", values="value").reset_index()

expected_columns = ["timestamp", "soil_moisture", "soil_temperature", "temperature", "humidity", "barometric_pressure", "co2", "light_intensity"]
df = df.reindex(columns=expected_columns)
df = df.ffill()


df["timestamp"] = pd.to_datetime(df["timestamp"])

df["time_since_last"] = df["timestamp"].diff().dt.total_seconds().fillna(0)
TIME_THRESHOLD = 120
df = df[df["time_since_last"] <= TIME_THRESHOLD]

df["temp_change"] = df["temperature"].diff().fillna(0)

df["soil_moisture_adjusted"] = df["soil_moisture"].rolling(window=1440, min_periods=1).mean()

MIN_MOISTURE = 10
MAX_MOISTURE = 100
df["soil_moisture_adjusted"] = df["soil_moisture_adjusted"].clip(lower=MIN_MOISTURE, upper=MAX_MOISTURE)
df["soil_moisture_adjusted"] = df["soil_moisture_adjusted"].mask(df["soil_moisture_adjusted"].diff().abs() > 20, df["soil_moisture_adjusted"].shift())

threshold = 30
future_dry_times = []

for i in range(len(df)):
    current_time = df.iloc[i]["timestamp"]
    future = df.iloc[i + 1:]
    below = future[future["soil_moisture_adjusted"] < threshold]
    if not below.empty:
        dry_timestamp = below.iloc[0]["timestamp"]
        future_dry_times.append(dry_timestamp)
    else:
        future_dry_times.append(None)

df["dry_timestamp"] = future_dry_times
df = df.dropna(subset=["dry_timestamp"])
df["time_until_dry"] = (df["dry_timestamp"] - df["timestamp"]).dt.total_seconds()


selected_features = ["temperature", "temp_change", "humidity", "time_since_last", "soil_temperature"]
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X = scaler_X.fit_transform(df[selected_features].values)
y = scaler_y.fit_transform(df["time_until_dry"].values.reshape(-1, 1))

final_df = df[selected_features + ["time_until_dry", "dry_timestamp"]]
final_df.to_csv("processed_data.csv", index=False)
print("✅ Processed data saved with dry timestamps")

plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["soil_moisture_adjusted"], label="Adjusted Soil Moisture", color="blue")
plt.xlabel("Time")
plt.ylabel("Soil Moisture")
plt.title("Soil Moisture Trend Over Time (With Dry Forecast)")
plt.legend()
plt.xticks(rotation=45)
plt.show()
