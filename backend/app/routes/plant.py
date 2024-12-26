from flask import Blueprint, jsonify, current_app, request
from app.models import Plant
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

plant_bp = Blueprint('plant', __name__)

@plant_bp.route('/get_plant', methods=['GET'])
def get_plant():
	try:
		if "plant" not in current_app.config['DB'].list_collection_names():
			return jsonify({})

		plant = list(current_app.config['DB']["plant"].find({}))
		return jsonify(plant)
	except Exception as e:
		logger.error(f"Error getting plant collection: {e}")
		return {"error": "Failed to retrieve plant collection"}, 500

@plant_bp.route('/create_plant', methods=['POST'])
def new_plant():
	data = request.json
	Plant.create(name=data.name, plant_type_id=data.plant_type, thresholds=data.thresholds, sensors=list(current_app.config['DB']["sensors"].find({})))