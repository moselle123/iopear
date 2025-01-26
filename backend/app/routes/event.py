from flask import Blueprint, jsonify, request
import logging
from app.models import Event
from app.models import Notification
from app.services.event_manager import load_rules

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
		event_id = Event.create(name=data["name"], sensor_id=data["sensor_id"], measurement=data["measurement"], conditions=data["conditions"], logic=data["logic"], is_enabled=data["is_enabled"])
		load_rules(event_id)
		return {"message": "Event created"}, 201
	except Exception as e:
		logger.error(f"Error creating event: {e}")
		return {"error": "Failed to create event"}, 500

@event_bp.route('/update_event/<event_id>', methods=['PUT'])
def update_event(event_id):
	data = request.json
	try:
		message = Event.update(event_id, data)
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
		Notification.delete_notifications_by_entity(event_id)
		return {"message": "Event deleted"}, 200
	except Exception as e:
		logger.error(f"Error deleting event: {e}")
		return {"error": "Failed to delete event"}, 500
