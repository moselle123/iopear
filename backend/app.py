import os
from flask import Flask, render_template, jsonify
import logging
from pymongo import MongoClient
from services.i2c_manager import I2CManager
from models import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='templates/assets')

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/iopear_db")
client = MongoClient(mongo_uri)
db = client.io_pear_db
if "plant_types" not in db.list_collection_names():
	PlantType.create(db, name="Monstera Deliciousa", nicknames=["Cheese Plant"], thresholds={"soilMoisture": 20, "temperature": 30, "lux": 800})
	PlantType.create(db, name="Zanzibar Gem", nicknames=["ZZ Plant"], thresholds={"soilMoisture": 20, "temperature": 30, "lux": 800})

i2c_manager = I2CManager()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
	
@app.route('/', methods=('GET', 'POST'))
def index():
	return render_template('index.html')

@app.route("/get_sensor_data")
def get_sensor_data():
	try:
		sensor_data = i2c_manager.read_sensors()
		return jsonify(sensor_data)
	except Exception as e:
		logger.error(f"Error getting sensor data: {e}")
		return {"error": "Failed to retrieve sensor data"}, 500
	
@app.route('/get_plant_types', methods=['GET'])
def get_plant_types():
	try:
		plant_types = list(db["plant_types"].find({}))
		for plant in plant_types:
			plant["_id"] = str(plant["_id"])
		
		return jsonify(plant_types)
	except Exception as e:
		logger.error(f"Error getting plant types data: {e}")
		return {"error": "Failed to retrieve plant types"}, 500
	
