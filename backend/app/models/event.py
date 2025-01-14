from bson import ObjectId
from flask import current_app

class Event:
	@staticmethod
	def create(sensor_id, measurement, condition, threshold, active):
		result = current_app.config['DB']["event"].insert_one({"sensor_id": ObjectId(sensor_id), "measurement": measurement, "condition": condition, "threshold": threshold, "active": active})
		return result.inserted_id

	@staticmethod
	def delete(event_id):
		result = current_app.config['DB']["event"].delete_one({"_id": ObjectId(event_id)})
		return result.deleted_count

	@staticmethod
	def get_events_by_measurement(measurement):
		return current_app.config['DB']["event"].find({"measurement": measurement, "active": True})

	@staticmethod
	def create_event_instance(sensor_id, value, timestamp):
		result = current_app.config['DB']["event_instance"].insert_one({"event_id": ObjectId(sensor_id), "value": value, "timestamp": timestamp})
		return result.inserted_id