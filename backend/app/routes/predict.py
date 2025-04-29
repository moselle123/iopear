from flask import Blueprint, jsonify, current_app
from app.services.moisture_prediction import predict_soil_moisture
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict_endpoint():
	try:
		latest_readings = current_app.config['SENSOR_MANAGER'].get_last_readings()
		temp_change = current_app.config['SENSOR_MANAGER'].get_temp_change()

		if not (latest_readings or temp_change):
			return jsonify({"System has not collected enough data for a prediction yet"}), 500

		prediction = predict_soil_moisture({
				"temperature": latest_readings["temperature"],
				"humidity": latest_readings["humidity"],
				"time_since_last": 60,
				"temp_change": temp_change,
			})
		return jsonify({"predicted_soil_moisture": prediction})

	except Exception as e:
		logger.error(f"Error getting soil moisture prediction: {e}")
		return jsonify({"error": "Error getting soil moisture prediction"}), 500
