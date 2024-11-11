import signal
import logging
from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient
from app.services.i2c_manager import I2CManager
from models import *
from routes import *
from app.config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
	app = Flask(__name__, static_folder='templates/assets')
	app.config.from_object(config_class)
	CORS(app, origins=["http://localhost:5173", "http://192.168.4.116:5173", "100.103.241.41:5173"])

	mongo_client = MongoClient(app.config['MONGO_URI'])
	app.config['DB_CLIENT'] = mongo_client
	app.config['DB'] = mongo_client.io_pear_db

	i2c_manager = I2CManager(app.config['DB'])
	app.config['I2C_MANAGER'] = i2c_manager

	if "plant_types" not in app.config['DB'].list_collection_names():
		PlantType.create(name="Monstera Deliciousa", nicknames=["Cheese Plant"], thresholds={"soil_moisture": [20, 100], "soil_temperature": [26, 30], "humidity": [50, 60], "temperature": [24, 30], "lux": [800, 900]})
		PlantType.create(name="Zanzibar Gem", nicknames=["ZZ Plant"], thresholds={"soil_moisture": [20, 100], "soil_temperature": [26, 30], "humidity": [50, 60], "temperature": [24, 30], "lux": [800, 900]})

	if "plant" in app.config['DB'].list_collection_names():
		i2c_manager.start_reading()

	app.register_blueprint(plant_bp)
	app.register_blueprint(plant_type_bp)
	app.register_blueprint(sensor_bp)


	def signal_handler(sig, frame):
		logger.warning("Termination signal received. Stopping I2C manager.")
		i2c_manager.stop_reading()
		logger.warning("I2C manager stopped. Exiting application.")
		exit(0)

	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)

	@app.route('/', methods=('GET', 'POST'))
	def index():
		return render_template('index.html')

	return app
