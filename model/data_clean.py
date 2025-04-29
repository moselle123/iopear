import pandas as pd

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
print(df.head())

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["time_since_last"] = df["timestamp"].diff().dt.total_seconds().fillna(0)
df["temp_change"] = df["temperature"].diff().fillna(0)

selected_features = ["temperature", "temp_change", "humidity", "time_since_last"]
target = "soil_moisture"

X = df[selected_features].values
y = df[target].values.reshape(-1, 1)

