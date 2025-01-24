from bson import ObjectId
from flask import current_app
from datetime import datetime, timezone

class Sensor:
	def __init__(self, _id, name, enabled, calibration=None):
		self._id = _id
		self.name = name
		self.thresholds = {}
		self.enabled = enabled
		self.adafruit_instance = None
		if name == 'SS':
			self.calibration = calibration

	def to_dict(self):
		sensor = {
			"_id": str(self._id),
			"name": self.name,
			"enabled": self.enabled,
			"thresholds": self.thresholds
		}
		if self.calibration:
			sensor["calibration"] = self.calibration

		return sensor

	def update_calibration(self, min_val, max_val):
		if self.name == 'SS':
			self.calibration = {"min": min_val, "max": max_val}
			current_app.config['DB']["sensors"].update_one({"_id": ObjectId(self._id)}, {"$set": {"calibration": self.calibration}})

	def update_settings(self, enabled, thresholds):
		self.enabled = enabled
		self.thresholds = thresholds
		current_app.config['DB']["sensors"].update_one({"_id": ObjectId(self._id)}, {"$set": {"enabled": self.enabled, "thresholds": self.thresholds}})

	@classmethod
	def create(cls, name):
		sensor_data = current_app.config['DB']["sensors"].find_one({"name": name})
		if sensor_data:
			if sensor_data["name"] == "SS" and "calibration" in sensor_data:
				return cls(sensor_data["_id"], sensor_data["name"], sensor_data["enabled"], sensor_data["calibration"])
			return cls(sensor_data["_id"], sensor_data["name"], sensor_data["enabled"])

		result = current_app.config['DB']["sensors"].insert_one({"name": name, "enabled": True})
		return cls(result.inserted_id, name, True)

	@staticmethod
	def get_sensors():
		return current_app.config['DB']["sensors"].find()

	@classmethod
	def delete(cls, sensor_id):
		result = current_app.config['DB']["sensors"].delete_one({"_id": ObjectId(sensor_id)})
		return result.deleted_count
