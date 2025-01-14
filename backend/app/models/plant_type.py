from bson import ObjectId
from flask import current_app

class PlantType:
	@staticmethod
	def create(name, nicknames, thresholds, description):
		plant_data = {
			"name": name,
			"nicknames": nicknames,
			"thresholds": thresholds,
			"description": description,
		}
		result = current_app.config['DB']["plant_type"].insert_one(plant_data)
		plant_data["_id"] = str(result.inserted_id)
		return plant_data

	@staticmethod
	def get_by_id(plant_type_id):
		result = current_app.config['DB']["plant_type"].find_one({"_id": ObjectId(plant_type_id)})
		if not result:
			return None
		return {
			"_id": str(result["_id"]),
			"name": result["name"],
			"nicknames": result["nicknames"],
			"thresholds": result["thresholds"],
			"description": result["description"],
		}

	@staticmethod
	def delete(plant_type_id):
		result = current_app.config['DB']["plant_type"].delete_one({"_id": ObjectId(plant_type_id)})
		return result.deleted_count
