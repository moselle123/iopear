from bson import ObjectId
from flask import current_app

class Action:
	@staticmethod
	def create(name, actuator_id, actuator_state, duration=None):
		action_data = {
			"name": name,
			"actuator_id": ObjectId(actuator_id),
			"actuator_state": actuator_state,
			"last_triggered": None,
		}

		if duration:
			action_data["duration"] = duration

		result = current_app.config['DB']["action"].insert_one(action_data)
		return result.inserted_id

	@staticmethod
	def update(action_id, updated_fields):
		result = current_app.config['DB']["action"].update_one({"_id": ObjectId(action_id)}, {"$set": updated_fields})

		if result.matched_count == 0:
			return {"success": False, "message": "action not found"}
		if result.modified_count == 0:
			return {"success": True, "message": "No changes were made to the action"}

		return {"success": True, "message": "action updated successfully"}

	@staticmethod
	def delete(action_id):
		result = current_app.config['DB']["action"].delete_one({"_id": ObjectId(action_id)})
		return result.deleted_count

	@staticmethod
	def get_actions():
		return current_app.config['DB']["action"].find()
