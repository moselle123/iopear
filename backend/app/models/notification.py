from bson import ObjectId
from flask import current_app

class Notification:
	@staticmethod
	def create(event_id, value, timestamp):
		result = current_app.config['DB']["notification"].insert_one({"event_id": ObjectId(event_id), "value": value, "timestamp": timestamp})
		return result.inserted_id

	@staticmethod
	def get_notifications_by_date_range(start_date, end_date):
		instances = current_app.config['DB']["notification"].find({"timestamp": {"$gte": start_date, "$lte": end_date}})
		return instances
