from flask import Blueprint, jsonify, current_app, request
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sensors_bp = Blueprint('sensors', __name__)

@sensors_bp.route("/get_sensor_data")
def get_sensor_data():
	try:
		return jsonify(current_app.config['I2C_MANAGER'].get_last_readings())
	except Exception as e:
		logger.error(f"Error getting sensor data: {e}")
		return {"error": "Failed to retrieve sensor data"}, 500

@sensors_bp.route('/get_sensors', methods=['GET'])
def get_sensors():
	try:
		sensors = list(current_app.config['DB']["sensors"].find({}))
		for sensor in sensors:
			sensor["_id"] = str(sensor["_id"])

		return jsonify(sensors)
	except Exception as e:
		logger.error(f"Error getting sensors collection: {e}")
		return {"error": "Failed to retrieve sensors collection"}, 500

@sensors_bp.route('/get_calibration_reading', methods=['GET'])
def get_calibration_reading():
	try:
		return jsonify({"soil_moisture": current_app.config['I2C_MANAGER'].get_soil_moisture()})
	except Exception as e:
		logger.error(f"Error getting soil moisture: {e}")
		return {"error": "Failed to retrieve soil moisture"}, 500

@sensors_bp.route('/calibrate_soil_moisture_sensor', methods=['POST'])
def calibrate_soil_moisture_sensor():
	data = request.json
	current_app.config['I2C_MANAGER'].ss.update_calibration(data[0], data[1])
	return jsonify({"message": "Calibration updated successfully"}), 200
