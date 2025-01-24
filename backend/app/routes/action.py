from flask import Blueprint, jsonify, request
import logging
from app.models import Action
from app.models import Notification
from app.services import ActionManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

action_bp = Blueprint('action', __name__)

@action_bp.route('/get_actions', methods=['GET'])
def get_actions():
	try:
		actions = list(Action.get_actions())
		for action in actions:
			action["_id"] = str(action["_id"])
			action["actuator_id"] = str(action["actuator_id"])

		return jsonify(actions)

	except Exception as e:
		logger.error(f"Error getting actions data: {e}")
		return {"error": "Failed to retrieve actions"}, 500

@action_bp.route('/create_action', methods=['POST'])
def create_action():
	data = request.json
	try:
		Action.create(data["name"], data["actuator_id"], data["actuator_state"], data["duration"])
		ActionManager.update_action_list()
		return {"message": "action created"}, 201

	except Exception as e:
		logger.error(f"Error updating action: {e}")
		return {"error": "Failed to create action"}, 500

@action_bp.route('/update_action/<action_id>', methods=['PUT'])
def update_action(action_id):
	data = request.json
	try:
		message = Action.update(action_id, data)
		if not message["success"]:
			return {"message": message}, 404

		ActionManager.update_action_list()
		return {"message": message}, 200

	except Exception as e:
		logger.error(f"Error updating action: {e}")
		return {"error": "Failed to update action"}, 500

@action_bp.route('/delete_action/<action_id>', methods=['DELETE'])
def delete_action(action_id):
	try:
		Action.delete(action_id)
		Notification.delete_notifications_by_entity(action_id)
		ActionManager.update_action_list()
		return {"message": "action deleted"}, 200

	except Exception as e:
		logger.error(f"Error deleting action: {e}")
		return {"error": "Failed to delete action"}, 500

@action_bp.route('/trigger_action/<action_id>', methods=['POST'])
def trigger_action(action_id):
	try:
		ActionManager.trigger_action(action_id)
		return {"message": "Action triggered"}, 200

	except Exception as e:
		logger.error(f"Error triggering action: {e}")
		return {"error": "Failed to trigger action"}, 500
