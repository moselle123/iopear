from bson import ObjectId
from flask import current_app

class Plant:
	def __init__(self, name, plant_type_id, thresholds, sensors):
		self.name = name
		self.plant_type_id = plant_type_id
		self.thresholds = thresholds
		self.sensors = sensors

	def to_dict(self):
		return {
			"name": self.name,
			"plant_type_id": self.plant_type_id,
			"thresholds": self.thresholds,
			"sensors": self.sensors,
		}

	@classmethod
	def create(cls, name, plant_type_id, thresholds):
		sensors = list(current_app.config['DB']["sensors"].find({}))
		plant = cls(name, plant_type_id, thresholds, sensors)
		result = current_app.config['DB']["plants"].insert_one(plant.to_dict())
		return result.inserted_id

	@classmethod
	def get_by_id(cls, plant_id):
		plant_data = current_app.config['DB']["plant"].find_one({"_id": ObjectId(plant_id)})
		return plant_data

	@classmethod
	def delete(cls, plant_id):
		result = current_app.config['DB']["plant"].delete_one({"_id": ObjectId(plant_id)})
		return result.deleted_count
