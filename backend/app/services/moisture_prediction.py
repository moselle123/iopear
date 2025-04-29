import torch
import joblib
import pandas as pd
from model.training import LinearRegressionModel
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(BASE_DIR)

scaler_X = joblib.load("../../../model/scaler_X.pkl")
scaler_y = joblib.load("../../../model/scaler_y.pkl")

model = LinearRegressionModel(4)
model.load_state_dict(torch.load("../../../model/soil_moisture_model.pth"))
model.eval()

def predict_soil_moisture(readings):
	features = ["temperature", "temp_change", "humidity", "time_since_last"]
	df = pd.DataFrame([readings], columns=features)

	X_scaled = scaler_X.transform(df)

	input_tensor = torch.tensor(X_scaled, dtype=torch.float32)
	predicted = model(input_tensor).detach().numpy()

	predicted = scaler_y.inverse_transform(predicted)[0][0]

	return round(predicted, 2)
