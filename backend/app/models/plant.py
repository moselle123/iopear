from bson import ObjectId
from flask import current_app

class Plant:
	def __init__(self, name, plant_type_id, thresholds, sensors):
		self.name = name
		self.plant_type_id = plant_type_id
		self.thresholds = thresholds
		self.sensors = sensors

	@classmethod
	def to_dict(cls):
		plant = current_app.config['DB']["plant"].find_one({})
		plant['id'] = str(plant['_id'])
		plant['plant_type_id'] = str(plant['plant_type_id'])
		for sensor in plant['sensors']:
			sensor['_id'] = str(sensor['_id'])

		return {
			"_id": plant['id'],
			"name": plant['name'],
			"plant_type_id": plant['plant_type_id'],
			"thresholds": plant['thresholds'],
			"sensors": plant['sensors'],
		}

	@classmethod
	def create(cls, name, plant_type_id, thresholds):
		sensors = list(current_app.config['DB']["sensors"].find({}))
		plant = cls(name, plant_type_id, thresholds, sensors)
		result = current_app.config['DB']["plant"].insert_one(plant.to_dict())
		return result.inserted_id

	@classmethod
	def get_by_id(cls, plant_id):
		plant_data = current_app.config['DB']["plant"].find_one({"_id": ObjectId(plant_id)})
		return plant_data

	@classmethod
	def delete(cls, plant_id):
		result = current_app.config['DB']["plant"].delete_one({"_id": ObjectId(plant_id)})
		return result.deleted_count
