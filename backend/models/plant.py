from bson import ObjectId

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
	def create(cls, db, name, plant_type_id, thresholds):
		plant = cls(name, plant_type_id, thresholds, [])
		result = db["plants"].insert_one(plant.to_dict())
		return result.inserted_id

	@classmethod
	def get_by_id(cls, db, plant_id):
		plant_data = db["plant"].find_one({"_id": ObjectId(plant_id)})
		return plant_data

	@classmethod
	def delete(cls, db, plant_id):
		result = db["plant"].delete_one({"_id": ObjectId(plant_id)})
		return result.deleted_count
