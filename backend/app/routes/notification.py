from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from app.models import Notification

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/get_notifications', methods=['GET'])
def get_notifications():
	try:
		start_date = request.args.get('start_date')
		end_date = request.args.get('end_date')

		if not start_date or not end_date:
			return jsonify({"error": "start_date and end_date are required"}), 400

		start_date = start_date.replace("Z", "+00:00")
		end_date = end_date.replace("Z", "+00:00")

		try:
			start_date = datetime.fromisoformat(start_date)
			end_date = datetime.fromisoformat(end_date)

			notifications = list(Notification.get_notifications_by_date_range(start_date, end_date))
			for instance in notifications:
				instance["_id"] = str(instance["_id"])
				instance["entity_id"] = str(instance["entity_id"])

			return jsonify(notifications)
		except ValueError:
			return jsonify({"error": "Invalid date format. Use ISO format"}), 400

	except Exception as e:
		logger.error(f"Error getting notifications: {e}")
		return {"error": "Failed to retrieve notifications"}, 500