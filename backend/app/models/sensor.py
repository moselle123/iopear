from bson import ObjectId
from flask import current_app
from app.models.event import Event
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
		self.update_associated_events()

	def update_associated_events(self):
		for measurement, (lower, upper) in self.thresholds.items():
			lower_event_name = f"{self.name} {measurement} Below Threshold"
			upper_event_name = f"{self.name} {measurement} Above Threshold"

			lower_condition = {"measurement": measurement, "type": "less_than", "value": lower}
			upper_condition = {"measurement": measurement, "type": "greater_than", "value": upper}

			existing_lower_event = current_app.config['DB']["event"].find_one({"name": lower_event_name})
			existing_upper_event = current_app.config['DB']["event"].find_one({"name": upper_event_name})

			if existing_lower_event:
				Event.update(existing_lower_event["_id"], {"conditions": [lower_condition]})
			else:
				Event.create(lower_event_name, [lower_condition], "AND", [], True, None, is_threshold_event=True)

			if existing_upper_event:
				Event.update(existing_upper_event["_id"], {"conditions": [upper_condition]})
			else:
				Event.create(upper_event_name, [upper_condition], "AND", [], True, None, is_threshold_event=True)

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
