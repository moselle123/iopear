import torch
import torch.optim as optim
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from linear_regression_model import LinearRegressionModel

def train_model():
	df = pd.read_csv("processed_data.csv")

	selected_features = ["temperature", "temp_change", "humidity", "time_since_last"]
	target = "soil_moisture_adjusted"

	X = df[selected_features].values
	y = df[target].values.reshape(-1, 1)

	scaler_X = StandardScaler()
	scaler_y = StandardScaler()
	X = scaler_X.fit_transform(X)
	y = scaler_y.fit_transform(y)

	joblib.dump(scaler_X, "scaler_X.pkl")
	joblib.dump(scaler_y, "scaler_y.pkl")

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
	X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
	y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
	X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
	y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

	input_size = len(selected_features)
	model = LinearRegressionModel(input_size)

	criterion = nn.MSELoss()
	optimizer = optim.Adam(model.parameters(), lr=0.001)


	epochs = 2000
	for epoch in range(epochs):
		model.train()

		predictions = model(X_train_tensor)
		loss = criterion(predictions, y_train_tensor)

		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

		if epoch % 50 == 0:
			print(f"Epoch {epoch}, Loss: {loss.item()}")

	torch.save(model.state_dict(), "soil_moisture_model.pth")

	model.eval()
	with torch.no_grad():
		y_test_pred = model(X_test_tensor).numpy()
		y_test_actual = y_test_tensor.numpy()

	y_test_pred = scaler_y.inverse_transform(y_test_pred)
	y_test_actual = scaler_y.inverse_transform(y_test_actual)

	rmse = np.sqrt(mean_squared_error(y_test_actual, y_test_pred))
	mae = mean_absolute_error(y_test_actual, y_test_pred)
	r2 = r2_score(y_test_actual, y_test_pred)

	print(f"RMSE: {rmse:.3f}")
	print(f"MAE: {mae:.3f}")
	print(f"R² Score: {r2:.3f}")
