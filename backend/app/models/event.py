from bson import ObjectId
from flask import current_app

class Event:
	@staticmethod
	def create(name, conditions, logic, actions, is_enabled, scheduled_time):
		for condition in conditions:
			condition["value"] = float(condition["value"])
		result = current_app.config['DB']["event"].insert_one({"name": name, "conditions": conditions, "logic": logic, "scheduled_time": scheduled_time, "is_enabled": is_enabled, "actions": actions, "last_triggered": None})
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
	def get_events(id=None, enabled=None):
		query = {}

		if enabled:
			query["is_enabled"] = enabled
		if id:
			query["_id"] = ObjectId(id)
			return current_app.config['DB']["event"].find_one(query)

		return list(current_app.config['DB']["event"].find(query))
