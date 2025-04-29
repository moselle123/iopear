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

# create a time since last reading column
df["time_since_last"] = df["timestamp"].diff().dt.total_seconds().fillna(0)
TIME_THRESHOLD = 120
df = df[df["time_since_last"] <= TIME_THRESHOLD]

# create a temperate change column (temperature change since last reading)
df["temp_change"] = df["temperature"].diff().fillna(0)

# average the soil moisture to reduce noise (due to rubbish sensor)
df["soil_moisture_adjusted"] = df["soil_moisture"].rolling(window=1440, min_periods=1).mean()

MIN_MOISTURE = 10
MAX_MOISTURE = 100
df["soil_moisture_adjusted"] = df["soil_moisture_adjusted"].clip(lower=MIN_MOISTURE, upper=MAX_MOISTURE)

# replace spikes in data with previous values:
df["soil_moisture_adjusted"] = df["soil_moisture_adjusted"].mask(df["soil_moisture_adjusted"].diff().abs() > 20, df["soil_moisture_adjusted"].shift())

selected_features = ["temperature", "temp_change", "humidity", "time_since_last", "soil_temperature"]
target = "soil_moisture_adjusted"

scaler_X = StandardScaler()
scaler_y = StandardScaler()
X = scaler_X.fit_transform(df[selected_features].values)
y = scaler_y.fit_transform(df[target].values.reshape(-1, 1))

df.to_csv("processed_data.csv", index=False)
print("Processed data saved")

plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["soil_moisture_adjusted"], label="Adjusted Soil Moisture", color="blue")
plt.xlabel("Time")
plt.ylabel("Soil Moisture")
plt.title("Soil Moisture Trend Over Time (After Fixes)")
plt.legend()
plt.xticks(rotation=45)
plt.show()
