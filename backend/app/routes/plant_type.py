from flask import Blueprint, jsonify, current_app
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

plant_type_bp = Blueprint('plant_type', __name__)
db = current_app.config['DB']

@plant_type_bp.route('/get_plant_types', methods=['GET'])
def get_plant_types():
	try:
		plant_types = list(db["plant_types"].find({}))
		for plant in plant_types:
			plant["_id"] = str(plant["_id"])

		return jsonify(plant_types)
	except Exception as e:
		logger.error(f"Error getting plant types data: {e}")
		return {"error": "Failed to retrieve plant types"}, 500