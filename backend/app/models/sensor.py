from bson import ObjectId
from Flask import current_app

class Sensor:
	def __init__(self, _id, name, readings):
		self._id = _id
		self.name = name
		self.readings = readings
		if name == 'Soil_Moisture_Sensor':
			self.calibration = None

	def to_dict(self):
		return {
			"_id": self._id,
			"name": self.name,
			"readings": self.readings[:100],
		}

	def add_reading(self, reading):
		if self.name == 'Soil_Moisture_Sensor':
			if self.calibration != None:
				reading = {"soil_moisture": (reading - self.calibration.min) / (self.calibration.max - self.calibration.min) * 100}
			else:
				reading = {"soil_moisture": 0}

		self.readings.append(reading)
		current_app.config['DB']["sensors"].update_one({"_id": ObjectId(self._id)}, {"$push": {"readings": reading}})

	def update_calibration(self, min_val, max_val):
		if self.name == 'Soil_Moisture_Sensor':
			self.calibration = {"min": min_val, "max": max_val}
			current_app.config['DB']["sensors"].update_one({"_id": ObjectId(self._id)}, {"$set": {"calibration": self.calibration}})

	@classmethod
	def create(cls, name):
		sensor_data = current_app.config['DB']["sensors"].find_one({"name": name})
		if sensor_data:
			return cls(sensor_data["_id"], sensor_data["name"], sensor_data["readings"])

		result = current_app.config['DB']["sensors"].insert_one({"name": name, "readings": []})
		return cls(result.inserted_id, name, [])

	@classmethod
	def get_by_id(cls, sensor_id):
		sensor_data = current_app.config['DB']["sensors"].find_one({"_id": ObjectId(sensor_id)})
		return sensor_data

	@classmethod
	def delete(cls, sensor_id):
		result = current_app.config['DB']["sensors"].delete_one({"_id": ObjectId(sensor_id)})
		return result.deleted_count
