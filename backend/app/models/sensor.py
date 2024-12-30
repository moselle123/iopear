from bson import ObjectId
from flask import current_app
from datetime import datetime, timezone

class Sensor:
	def __init__(self, _id, name):
		self._id = _id
		self.name = name
		self.adafruit_instance = None
		if name == 'SS':
			self.calibration = None

	def to_dict(self):
		return {
			"_id": str(self._id),
			"name": self.name,
		}

	def update_calibration(self, min_val, max_val):
		if self.name == 'SS':
			self.calibration = {"min": min_val, "max": max_val}
			current_app.config['DB']["sensors"].update_one({"_id": ObjectId(self._id)}, {"$set": {"calibration": self.calibration}})

	@classmethod
	def create(cls, name):
		sensor_data = current_app.config['DB']["sensors"].find_one({"name": name})
		if sensor_data:
			return cls(sensor_data["_id"], sensor_data["name"])

		result = current_app.config['DB']["sensors"].insert_one({"name": name})
		return cls(result.inserted_id, name)

	@classmethod
	def get_by_id(cls, sensor_id):
		sensor_data = current_app.config['DB']["sensors"].find_one({"_id": ObjectId(sensor_id)})
		return sensor_data

	@classmethod
	def delete(cls, sensor_id):
		result = current_app.config['DB']["sensors"].delete_one({"_id": ObjectId(sensor_id)})
		return result.deleted_count

	# readings functionality
	def create_reading(self, measurement, unit, value):
		if self.name == 'SS' and self.calibration:
			value = (value - self.calibration['min']) / (self.calibration['max'] - self.calibration['min']) * 100

		reading = {
			"sensor_id": ObjectId(self._id),
			"timestamp": datetime.now(timezone.utc),
			"value": value,
			"unit": unit,
			"measurement": measurement,
		}

		current_app.config['DB']["reading"].insert_one(reading)

	def get_readings(self, limit=100, skip=0):
		readings_cursor = current_app.config['DB']["reading"].find({"sensor_id": ObjectId(self._id)}).sort("timestamp", -1).skip(skip).limit(limit)

		return [
			{
				"_id": str(reading["_id"]),
				"sensor_id": str(reading["sensor_id"]),
				"timestamp": reading["timestamp"].isoformat(),
				"value": reading["value"],
				"unit": reading["unit"],
				"measurement": reading["measurement"],
			}
			for reading in readings_cursor
		]

	def get_latest_reading(self):
		reading = current_app.config['DB']["reading"].find_one({"sensor_id": ObjectId(self._id)}, sort=[("timestamp", -1)])
		if reading:
			return {
				"_id": str(reading["_id"]),
				"sensor_id": str(reading["sensor_id"]),
				"timestamp": reading["timestamp"].isoformat(),
				"value": reading["value"],
				"unit": reading["unit"],
				"measurement": reading["measurement"],
			}
		return None

	def get_readings_by_date_range(self, start_date, end_date):
		readings_cursor = current_app.config['DB']["reading"].find({
			"sensor_id": ObjectId(self._id),
			"timestamp": {"$gte": start_date, "$lte": end_date}
		}).sort("timestamp", -1)

		return [
			{
				"_id": str(reading["_id"]),
				"sensor_id": str(reading["sensor_id"]),
				"timestamp": reading["timestamp"].isoformat(),
				"value": reading["value"],
				"unit": reading["unit"],
				"measurement": reading["measurement"],
			}
			for reading in readings_cursor
		]

	def get_readings_by_measurement(self, measurement, limit=100, skip=0):
		readings_cursor = current_app.config['DB']["reading"].find(
			{"sensor_id": ObjectId(self._id), "measurement": measurement}
		).sort("timestamp", -1).skip(skip).limit(limit)

		return [
			{
				"_id": str(reading["_id"]),
				"sensor_id": str(reading["sensor_id"]),
				"timestamp": reading["timestamp"].isoformat(),
				"value": reading["value"],
				"unit": reading["unit"],
				"measurement": reading["measurement"],
			}
			for reading in readings_cursor
		]
