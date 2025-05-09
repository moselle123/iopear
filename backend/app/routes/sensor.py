from flask import Blueprint, jsonify, current_app, request
import logging
from app.models.sensor import Sensor
from app.services.sensor_registry import SensorRegistry

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sensor_bp = Blueprint('sensor', __name__)

@sensor_bp.route('/get_sensors', methods=['GET'])
def get_sensors():
	try:
		sensors = list(Sensor.get_sensors())
		for sensor in sensors:
			sensor["_id"] = str(sensor["_id"])

		return jsonify(sensors)
	except Exception as e:
		logger.error(f"Error getting sensors collection: {e}")
		return {"error": "Failed to retrieve sensors collection"}, 500

@sensor_bp.route('/get_calibration_reading', methods=['GET'])
def get_calibration_reading():
	try:
		return jsonify({"soil_moisture": current_app.config['SENSOR_MANAGER'].get_soil_moisture()})
	except Exception as e:
		logger.error(f"Error getting soil moisture: {e}")
		return {"error": "Failed to retrieve soil moisture"}, 500

@sensor_bp.route('/calibrate_soil_moisture_sensor', methods=['POST'])
def calibrate_soil_moisture_sensor():
	data = request.json
	if not data or not isinstance(data, (list, tuple)) or not len(data) == 2:
		return jsonify({"error": "Calibration data was not given in the expected format"}), 400
	try:
		ss = SensorRegistry.get_sensor("SS")
		ss.update_calibration(data[0], data[1])
		return jsonify({"message": "Calibration updated successfully"}), 200
	except Exception as e:
		logger.error(f"Error setting soil moisture calibration settings: {e}")
		return {"error": "Failed to calibrate soil moisture sensor."}, 500

@sensor_bp.route('/sensor/<sensor_name>/update_settings', methods=['PUT'])
def update_settings(sensor_name):
	data = request.json
	if 'enabled' not in data or 'thresholds' not in data:
		return {"error": "'enabled' and 'thresholds' are required fields."}, 400
	try:
		sensor = SensorRegistry.get_existing_sensor(sensor_name)
		if not sensor:
			return {"error": "Sensor not found"}, 404

		sensor.update_settings(data["enabled"], data["thresholds"])
		return jsonify({"message": "Sensor settings updated successfully"}), 200
	except Exception as e:
		logger.error(f"Error updating sensor settings: {e}")
		return {"error": "Failed to update sensor settings."}, 500
