from bson import ObjectId

class Sensor:
	def __init__(self, db, _id, name, readings):
		self.db = db
		self._id = _id
		self.name = name
		self.readings = readings

	def to_dict(self):
		return {
			"_id": self._id,
			"name": self.name,
			"readings": self.readings[:100],
		}
	
	def add_reading(self, reading):
		self.readings.append(reading)
		self.db["sensors"].update_one({"_id": ObjectId(self._id)}, {"$push": {"readings": reading}})

	@classmethod
	def create(cls, db, name):
		sensor_data = db["sensors"].find_one({"name": name})
		if sensor_data:
			return cls(db, sensor_data["_id"], sensor_data["name"], sensor_data["readings"])
		
		result = db["sensors"].insert_one({"name": name, "readings": []})
		return cls(db, result.inserted_id, name, [])

	@classmethod
	def get_by_id(cls, db, sensor_id):
		sensor_data = db["sensors"].find_one({"_id": ObjectId(sensor_id)})
		return sensor_data

	@classmethod
	def delete(cls, db, sensor_id):
		result = db["sensors"].delete_one({"_id": ObjectId(sensor_id)})
		return result.deleted_count
