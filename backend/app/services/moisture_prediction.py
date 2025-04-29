import torch
import joblib
import pandas as pd
from app.ml.linear_regression_model import LinearRegressionModel

scaler_X = joblib.load("../ml/scaler_X.pkl")
scaler_y = joblib.load("../ml/scaler_y.pkl")

model = LinearRegressionModel(4)
model.load_state_dict(torch.load("../ml/soil_moisture_model.pth"))
model.eval()

def predict_soil_moisture(readings):
	features = ["temperature", "temp_change", "humidity", "time_since_last"]
	df = pd.DataFrame([readings], columns=features)

	X_scaled = scaler_X.transform(df)

	input_tensor = torch.tensor(X_scaled, dtype=torch.float32)
	predicted = model(input_tensor).detach().numpy()

	predicted = scaler_y.inverse_transform(predicted)[0][0]

	return round(predicted, 2)
