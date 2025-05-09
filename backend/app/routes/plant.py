from flask import Blueprint, jsonify, request
from app.models import Plant
from app.services import SensorRegistry
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
	try:
		if not data:
			return {"error": "Failed to create plant, no valid data was given."}, 400

		SensorRegistry.initialise_settings(data["settings"])

		plant_id = Plant.create(name=data['name'], plant_type_id=data['plantTypeId'])
		return {"message": "Created plant successfully.", "_id": str(plant_id)}, 201
	except Exception as e:
		logger.error(f"Error creating plant collection: {e}")
		return {"error": "Failed to create plant."}, 500
