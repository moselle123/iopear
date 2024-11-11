from bson import ObjectId
from Flask import current_app

class PlantType:
	def __init__(self, name, nicknames, thresholds):
		self.name = name
		self.nicknames = nicknames
		self.thresholds = thresholds

	def to_dict(self):
		return {
			"name": self.name,
			"nicknames": self.nicknames,
			"thresholds": self.thresholds,
		}

	@classmethod
	def create(cls, name, nicknames, thresholds):
		plant = cls(name, nicknames, thresholds)
		result = current_app.config['DB']["plant_types"].insert_one(plant.to_dict())
		return result.inserted_id

	@classmethod
	def get_by_id(cls, plant_id):
		plant_data = current_app.config['DB']["plant_types"].find_one({"_id": ObjectId(plant_id)})
		return plant_data

	@classmethod
	def delete(cls, plant_types_id):
		result = current_app.config['DB']["plant_types"].delete_one({"_id": ObjectId(plant_types_id)})
		return result.deleted_count
