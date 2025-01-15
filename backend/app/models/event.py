from bson import ObjectId
from flask import current_app

class Event:
	@staticmethod
	def create(sensor_id, measurement, condition, threshold, isActive):
		result = current_app.config['DB']["event"].insert_one({"sensor_id": ObjectId(sensor_id), "measurement": measurement, "condition": condition, "threshold": threshold, "isActive": isActive})
		return result.inserted_id

	@staticmethod
	def update(event_id, measurement, condition, threshold, isActive):
		result = current_app.config['DB']["event"].update_one({"_id": ObjectId(event_id)}, {"$set": {"measurement": measurement, "condition": condition, "threshold": threshold, "isActive": isActive}})
		return result.inserted_id

	@staticmethod
	def delete(event_id):
		result = current_app.config['DB']["event"].delete_one({"_id": ObjectId(event_id)})
		return result.deleted_count

	@staticmethod
	def get_events():
		return current_app.config['DB']["event"].find()

	@staticmethod
	def get_events_by_measurement(measurement):
		return current_app.config['DB']["event"].find({"measurement": measurement, "isActive": True})

	@staticmethod
	def create_event_instance(event_id, value, timestamp):
		result = current_app.config['DB']["event_instance"].insert_one({"event_id": ObjectId(event_id), "value": value, "timestamp": timestamp})
		return result.inserted_id

	@staticmethod
	def get_event_instances_by_date_range(start_date, end_date):
		instances = current_app.config['DB']["event_instance"].find({"$match": {"timestamp": {"$gte": start_date, "$lte": end_date}}})
		return instances