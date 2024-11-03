from bson import ObjectId

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
	def create(cls, db, name, nicknames, thresholds):
		plant = cls(name, nicknames, thresholds)
		result = db["plant_types"].insert_one(plant.to_dict())
		return result.inserted_id

	@classmethod
	def get_by_id(cls, db, plant_id):
		plant_data = db["plant_types"].find_one({"_id": ObjectId(plant_id)})
		return plant_data

	@classmethod
	def delete(cls, db, plant_types_id):
		result = db["plant_types"].delete_one({"_id": ObjectId(plant_types_id)})
		return result.deleted_count
