from bson import ObjectId
from flask import current_app

class Notification:
	@staticmethod
	def create(notification_type, entity_id, timestamp):
		result = current_app.config['DB']["notification"].insert_one({"notification_type": notification_type, "entity_id": ObjectId(entity_id), "timestamp": timestamp})
		return result.inserted_id

	@staticmethod
	def get_notifications_by_date_range(start_date, end_date):
		instances = current_app.config['DB']["notification"].find({"timestamp": {"$gte": start_date, "$lte": end_date}}).sort("timestamp", -1)
		return instances

	@staticmethod
	def delete_notifications_by_entity(entity_id):
		result = current_app.config['DB']["notification"].delete_many({"entity_id": ObjectId(entity_id)})
		return result.deleted_count
