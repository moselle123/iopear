import os
import torch
import joblib
from app.ml.model import LinearRegressionModel

_model = None
_scaler_X = None
_scaler_y = None

def load_assets():
	global _model, _scaler_X, _scaler_y
	if _model and _scaler_X and _scaler_y:
		return _model, _scaler_X, _scaler_y

	model_dir = os.path.join(os.path.dirname(__file__), "model_files")

	_scaler_X = joblib.load(os.path.join(model_dir, "scaler_X.pkl"))
	_scaler_y = joblib.load(os.path.join(model_dir, "scaler_y.pkl"))

	_model = LinearRegressionModel(4)
	_model.load_state_dict(torch.load(os.path.join(model_dir, "soil_moisture_model.pth")))
	_model.eval()

	return _model, _scaler_X, _scaler_y
