from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from app.models import Event

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

event_bp = Blueprint('event', __name__)

@event_bp.route('/get_events', methods=['GET'])
def get_events():
	try:
		events = list(Event.get_events())
		for event in events:
			event["_id"] = str(event["_id"])
			event["sensor_id"] = str(event["sensor_id"])

		return jsonify(events)
	except Exception as e:
		logger.error(f"Error getting events data: {e}")
		return {"error": "Failed to retrieve events"}, 500

@event_bp.route('/create_event', methods=['POST'])
def create_event():
	data = request.json
	try:
		Event.create(data["sensor_id"], data["measurement"], data["condition"], data["threshold"], data["is_enabled"])
		return {"message": "Event created"}, 201
	except Exception as e:
		logger.error(f"Error getting updating event: {e}")
		return {"error": "Failed to create event"}, 500

@event_bp.route('/update_event/<event_id>', methods=['PUT'])
def update_event(event_id):
	data = request.json
	try:
		Event.update(event_id, data["measurement"], data["condition"], data["threshold"], data["is_enabled"])
		return {"message": "Event updated"}, 200
	except Exception as e:
		logger.error(f"Error getting updating event: {e}")
		return {"error": "Failed to update event"}, 500

@event_bp.route('/delete_event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
	try:
		Event.delete(event_id)
		return {"message": "Event deleted"}, 200
	except Exception as e:
		logger.error(f"Error getting updating event: {e}")
		return {"error": "Failed to update event"}, 500

@event_bp.route('/get_event_instances', methods=['GET'])
def get_event_instances():
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

			event_instances = Event.get_event_instances_by_date_range(start_date, end_date)
			for instance in event_instances:
				instance["_id"] = str(instance["_id"])
				instance["event_id"] = str(instance["event_id"])

			return jsonify(event_instances)
		except ValueError:
			return jsonify({"error": "Invalid date format. Use ISO 8601 format"}), 400

	except Exception as e:
		logger.error(f"Error getting event instances: {e}")
		return {"error": "Failed to retrieve event instances"}, 500
