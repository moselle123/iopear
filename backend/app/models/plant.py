from bson import ObjectId
from flask import current_app

class Plant:
	@staticmethod
	def to_dict():
		plant = current_app.config['DB']["plant"].find_one({})
		if not plant:
			return {}
		plant['id'] = str(plant['_id'])
		plant['plant_type_id'] = str(plant['plant_type_id'])
		for sensor in plant['sensors']:
			sensor['_id'] = str(sensor['_id'])

		return {
			"_id": plant['id'],
			"name": plant['name'],
			"plant_type_id": plant['plant_type_id'],
			"sensors": plant['sensors'],
		}

	@staticmethod
	def create(name, plant_type_id):
		sensors = list(current_app.config['DB']["sensors"].find({}))
		plant_type_id = ObjectId(plant_type_id)

		result = current_app.config['DB']["plant"].insert_one({"name": name, "plant_type_id": ObjectId(plant_type_id), "sensors": sensors})
		return result.inserted_id

	@classmethod
	def delete(cls, plant_id):
		result = current_app.config['DB']["plant"].delete_one({"_id": ObjectId(plant_id)})
		return result.deleted_count
