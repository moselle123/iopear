from bson import ObjectId
from flask import current_app

class Event:
	@staticmethod
	def create(name, sensor_id, measurement, conditions, logic, threshold, is_enabled):
		threshold = float(threshold)
		result = current_app.config['DB']["event"].insert_one({"name": name, "sensor_id": ObjectId(sensor_id), "measurement": measurement, "conditions": conditions, "logic": logic, "threshold": threshold, "is_enabled": is_enabled, "actions": [], "last_triggered": None})
		return result.inserted_id

	@staticmethod
	def update(event_id, updated_fields):
		result = current_app.config['DB']["event"].update_one({"_id": ObjectId(event_id)}, {"$set": updated_fields})

		if result.matched_count == 0:
			return {"success": False, "message": "Event not found"}
		if result.modified_count == 0:
			return {"success": True, "message": "No changes were made to the event"}

		return {"success": True, "message": "Event updated successfully"}

	@staticmethod
	def delete(event_id):
		result = current_app.config['DB']["event"].delete_one({"_id": ObjectId(event_id)})
		return result.deleted_count

	@staticmethod
	def get_events(id=None, measurement=None, enabled=None):
		query = {}
		if id is not None:
			query["_id"] = id
		if measurement is not None:
			query["measurement"] = measurement
		if enabled is not None:
			query["enabled"] = enabled

		return current_app.config['DB']["event"].find(query)
