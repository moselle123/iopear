import torch
import pandas as pd
from app.ml.loader import load_assets

def predict_soil_moisture(reading_dict):
	model, scaler_X, scaler_y = load_assets()

	features = ["temperature", "temp_change", "humidity", "time_since_last"]
	df = pd.DataFrame([reading_dict], columns=features)

	X_scaled = scaler_X.transform(df)
	input_tensor = torch.tensor(X_scaled, dtype=torch.float32)

	prediction = model(input_tensor).detach().numpy()
	predicted_value = scaler_y.inverse_transform(prediction)[0][0]
	return round(predicted_value, 2)
