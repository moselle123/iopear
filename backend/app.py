import os
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import logging
from services.i2c_manager import I2CManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='templates/assets')

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/iopear_db")
client = MongoClient(mongo_uri)
db = client.io_pear
i2c_manager = I2CManager()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
	
# host frontend
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
