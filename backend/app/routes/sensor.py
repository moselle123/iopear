from flask import Blueprint, jsonify, current_app, request
from datetime import datetime
import logging
from app.services.sensor_registry import SensorRegistry

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

@sensors_bp.route('/sensor/<sensor_name>/readings', methods=['GET'])
def get_readings(sensor_name):
	try:
		limit = int(request.args.get('limit', 100))
		skip = int(request.args.get('skip', 0))
		sensor = SensorRegistry.get_sensor(sensor_name)
		if not sensor:
			return jsonify({"error": "Sensor not found"}), 404

		readings = sensor.get_readings(limit=limit, skip=skip)
		return jsonify(readings), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@sensors_bp.route('/sensor/<sensor_name>/latest_reading', methods=['GET'])
def get_latest_reading(sensor_name):
	try:
		sensor = SensorRegistry.get_sensor(sensor_name)
		if not sensor:
			return jsonify({"error": "Sensor not found"}), 404

		reading = sensor.get_latest_reading()
		if not reading:
			return jsonify({"error": "No readings found"}), 404

		return jsonify(reading), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@sensors_bp.route('/sensor/<sensor_name>/readings_by_date_range', methods=['GET'])
def get_readings_by_date_range(sensor_name):
	try:
		start_date = request.args.get('start_date')
		end_date = request.args.get('end_date')
		measurement = request.args.get('measurement')

		if not start_date or not end_date:
			return jsonify({"error": "start_date and end_date are required"}), 400

		start_date = start_date.replace("Z", "+00:00")
		end_date = end_date.replace("Z", "+00:00")

		try:
			start_date = datetime.fromisoformat(start_date)
			end_date = datetime.fromisoformat(end_date)
		except ValueError:
			return jsonify({"error": "Invalid date format. Use ISO 8601 format"}), 400

		sensor = SensorRegistry.get_sensor(sensor_name)
		if not sensor:
			return jsonify({"error": "Sensor not found"}), 404

		readings = sensor.get_readings_by_date_range(start_date, end_date, measurement)
		return jsonify(readings), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@sensors_bp.route('/sensor/<sensor_name>/readings_by_measurement', methods=['GET'])
def get_readings_by_measurement(sensor_name):
	try:
		measurement = request.args.get('measurement')
		if not measurement:
			return jsonify({"error": "Measurement parameter is required"}), 400

		limit = int(request.args.get('limit', 100))
		skip = int(request.args.get('skip', 0))

		sensor = SensorRegistry.get_sensor(sensor_name)
		if not sensor:
			return jsonify({"error": "Sensor not found"}), 404

		readings = sensor.get_readings_by_measurement(measurement, limit=limit, skip=skip)
		return jsonify(readings), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500
