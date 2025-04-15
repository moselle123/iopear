from flask import Blueprint, jsonify, request
import logging
from app.models import Event
from app.models import Notification
from app.services import EventManager
import bson

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

event_bp = Blueprint('event', __name__)

@event_bp.route('/get_events', methods=['GET'])
def get_events():
	try:
		events = list(Event.get_events())
		for event in events:
			event["_id"] = str(event["_id"])

		return jsonify(events)
	except Exception as e:
		logger.error(f"Error getting events data: {e}")
		return {"error": "Failed to retrieve events"}, 500

@event_bp.route('/create_event', methods=['POST'])
def create_event():
	data = request.json
	if not data:
		return {"error": "Failed to create event, no valid data was given."}, 400
	try:
		event_id = Event.create(name=data["name"], conditions=data["conditions"], logic=data["logic"], actions=data["actions"], scheduled_time=data["scheduled_time"], is_enabled=data["is_enabled"])
		EventManager.update_event_list(event_id)
		return {"message": "Event created"}, 201
	except Exception as e:
		logger.error(f"Error creating event: {e}")
		return {"error": "Failed to create event"}, 500

@event_bp.route('/update_event/<event_id>', methods=['PUT'])
def update_event(event_id):
	if not bson.ObjectId.is_valid(event_id):
		return {"message": "ID entered is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string."}, 400
	data = request.json
	try:
		message = Event.update(event_id, data)
		if not message["success"]:
			return {"message": message}, 404
		EventManager.update_event_list(event_id)
		return {"message": message}, 200
	except Exception as e:
		logger.error(f"Error updating event: {e}")
		return {"error": "Failed to update event"}, 500

@event_bp.route('/delete_event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
	try:
		event = Event.delete(event_id)
		if not event:
			return {"message": "No event found with the given ID."}, 404
		Notification.delete_notifications_by_entity(event_id)
		return {"message": "Event deleted"}, 200
	except Exception as e:
		logger.error(f"Error deleting event: {e}")
		return {"error": "Failed to delete event"}, 500
