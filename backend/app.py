import os
import signal
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
from pymongo import MongoClient
from services.i2c_manager import I2CManager
from models import *

# set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# mongo db setup
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/iopear_db")
client = MongoClient(mongo_uri)
db = client.io_pear_db
if "plant_types" not in db.list_collection_names():
	PlantType.create(db, name="Monstera Deliciousa", nicknames=["Cheese Plant"], thresholds={"soil_moisture": [20, 100], "soil_temperature": [26, 30], "humidity": [50, 60], "temperature": [24, 30], "lux": [800, 900]})
	PlantType.create(db, name="Zanzibar Gem", nicknames=["ZZ Plant"], thresholds={"soil_moisture": [20, 100], "soil_temperature": [26, 30], "humidity": [50, 60], "temperature": [24, 30], "lux": [800, 900]})

# initiate i2c manager and ensure safely closing of threads on docker signals
def signal_handler(sig, frame):
	logger.warning("Termination signal received. Stopping I2C manager.")
	i2c_manager.stop_reading()
	logger.warning("I2C manager stopped. Exiting application.")
	exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
#i2c_manager = I2CManager(db)

# flask
app = Flask(__name__, static_folder='templates/assets')
CORS(app, origins=["http://localhost:5173", "http://192.168.4.116:5173", "100.103.241.41:5173"])
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

@app.route('/', methods=('GET', 'POST'))
def index():
	return render_template('index.html')

@app.route("/get_sensor_data")
def get_sensor_data():
	try:
		return jsonify(i2c_manager.get_last_readings())
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

@app.route('/get_sensors', methods=['GET'])
def get_sensors():
	try:
		sensors = list(db["sensors"].find({}))
		for sensor in sensors:
			sensor["_id"] = str(sensor["_id"])

		return jsonify(sensors)
	except Exception as e:
		logger.error(f"Error getting sensors collection: {e}")
		return {"error": "Failed to retrieve sensors collection"}, 500

@app.route('/get_plant', methods=['GET'])
def get_plant():
	try:
		if "plant" not in db.list_collection_names():
			return jsonify({})

		plant = list(db["plant"].find({}))
		return jsonify(plant)
	except Exception as e:
		logger.error(f"Error getting plant collection: {e}")
		return {"error": "Failed to retrieve plant collection"}, 500
