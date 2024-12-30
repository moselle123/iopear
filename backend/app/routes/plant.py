from flask import Blueprint, jsonify, current_app, request
from app.models import Plant
from bson.json_util import dumps, loads
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

plant_bp = Blueprint('plant', __name__)

@plant_bp.route('/get_plant', methods=['GET'])
def get_plant():
	try:
		plant = Plant.to_dict()
		return jsonify(plant)
	except Exception as e:
		logger.error(f"Error getting plant collection: {e}")
		return {"error": "Failed to retrieve plant collection"}, 500

@plant_bp.route('/create_plant', methods=['POST'])
def new_plant():
	data = request.json
	Plant.create(name=data['name'], plant_type_id=data['plantTypeId'], thresholds=data['thresholds'])
	return {"message": "Created plant successfully."}, 200
