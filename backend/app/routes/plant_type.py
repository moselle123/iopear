from flask import Blueprint, jsonify, current_app
import logging
from app.models import PlantType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

plant_type_bp = Blueprint('plant_type', __name__)

@plant_type_bp.route('/get_plant_types', methods=['GET'])
def get_plant_types():
	try:
		plant_types = list(current_app.config['DB']["plant_type"].find({}))
		for plant in plant_types:
			plant["_id"] = str(plant["_id"])

		return jsonify(plant_types)
	except Exception as e:
		logger.error(f"Error getting plant types data: {e}")
		return {"error": "Failed to retrieve plant types"}, 500

@plant_type_bp.route('/get_plant_type/<plant_type_id>', methods=['GET'])
def get_plant_type(plant_type_id):
	try:
		plant_type = PlantType.get_by_id(plant_type_id)
		if not plant_type:
			return {"error": "Plant type not found"}, 404
		return jsonify(plant_type)
	except Exception as e:
		logger.error(f"Error getting plant types data: {e}")
		return {"error": "Failed to retrieve plant types"}, 500