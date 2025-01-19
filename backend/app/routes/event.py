from flask import Blueprint, jsonify, request
import logging
from app.models import Event
from app.models import Notification

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
		message = Event.update(event_id, data["measurement"], data["condition"], data["threshold"], data["is_enabled"])
		if not message["success"]:
			return {"message": message}, 404
		return {"message": message}, 200
	except Exception as e:
		logger.error(f"Error updating event: {e}")
		return {"error": "Failed to update event"}, 500

@event_bp.route('/delete_event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
	try:
		Event.delete(event_id)
		Notification.delete_notifications_by_event(event_id)
		return {"message": "Event deleted"}, 200
	except Exception as e:
		logger.error(f"Error deleting event: {e}")
		return {"error": "Failed to delete event"}, 500
