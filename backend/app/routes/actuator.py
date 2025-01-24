from flask import Blueprint, jsonify
import logging
from app.models import Actuator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

actuator_bp = Blueprint('actuator', __name__)

@actuator_bp.route('/get_actuators', methods=['GET'])
def get_actuators():
	try:
		actuators = list(Actuator.get_actuators())
		for actuator in actuators:
			actuator["_id"] = str(actuator["_id"])

		return jsonify(actuators)

	except Exception as e:
		logger.error(f"Error getting actions data: {e}")
		return {"error": "Failed to retrieve actions"}, 500
