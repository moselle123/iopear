from flask import Blueprint, jsonify, request
import logging
from app.models import Action
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

