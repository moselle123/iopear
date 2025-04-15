from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import logging
from app.services.sensor_registry import SensorRegistry
from app.models import Reading

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

reading_bp = Blueprint('reading', __name__)

@reading_bp.route('/sensor/<sensor_name>/readings_by_date_range', methods=['GET'])
def get_readings_by_date_range(sensor_name):
	try:
		start_date = request.args.get('start_date')
		end_date = request.args.get('end_date')
		measurement = request.args.get('measurement')

		if not (start_date or end_date or measurement):
			return jsonify({"error": "start_date, end_date and measurement are required"}), 400

		start_date = start_date.replace("Z", "+00:00")
		end_date = end_date.replace("Z", "+00:00")

		try:
			start_date = datetime.fromisoformat(start_date)
			end_date = datetime.fromisoformat(end_date)
		except ValueError:
			return jsonify({"error": "Invalid date format. Use ISO format"}), 400

		sensor = SensorRegistry.get_existing_sensor(sensor_name)
		if not sensor:
			return jsonify({"error": "Sensor not found"}), 404

		readings = Reading.get_readings_by_date_range(sensor._id, start_date, end_date, measurement)
		return jsonify(readings), 200
	except Exception as e:
		logger.error(f"Error getting readings by date range: {e}")
		return {"error": "Failed to get readings by date range."}, 500


@reading_bp.route('/sensor/<sensor_name>/readings_by_measurement', methods=['GET'])
def get_readings_by_measurement(sensor_name):
	try:
		measurement = request.args.get('measurement')
		if not measurement:
			return jsonify({"error": "Measurement parameter is required"}), 400

		limit = int(request.args.get('limit', 100))
		skip = int(request.args.get('skip', 0))

		sensor = SensorRegistry.get_existing_sensor(sensor_name)
		if not sensor:
			return jsonify({"error": "Sensor not found"}), 404

		readings = Reading.get_readings_by_measurement(sensor._id, measurement, limit=limit, skip=skip)
		return jsonify(readings), 200
	except Exception as e:
		logger.error(f"Error getting readings by date range: {e}")
		return {"error": "Failed to get readings by measurement"}, 500

@reading_bp.route('/reading/get_statistics', methods=['GET'])
def get_statistics():
	try:
		stats = Reading.get_statistics()
		if not stats:
			return jsonify({"message": "No data found for the past week"}), 404

		return jsonify(stats), 200

	except Exception as e:
		logger.error(f"Error getting statistics: {e}")
		return jsonify({"error": "Failed to get sensor statistics"}), 500