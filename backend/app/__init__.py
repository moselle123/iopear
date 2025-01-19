import signal
import logging
from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient
from app.services import *
from app.models import *
from app.routes import *
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

	i2c_manager = I2CManager(app)
	app.config['I2C_MANAGER'] = i2c_manager

	app.register_blueprint(plant_bp)
	app.register_blueprint(plant_type_bp)
	app.register_blueprint(sensor_bp)
	app.register_blueprint(reading_bp)
	app.register_blueprint(event_bp)
	app.register_blueprint(notification_bp)


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

	with app.app_context():
		i2c_manager._initialise_sensors()

		if "plant_type" not in app.config['DB'].list_collection_names():
			PlantType.create(name="Monstera Deliciousa", nicknames=["Cheese Plant"], thresholds={"soil_moisture": [20, 100], "soil_temperature": [26, 30], "humidity": [50, 60], "temperature": [24, 30], "light_intensity": [800, 900], "barometric_pressure": [960, 1050], "co2": [400, 1000]}, description="The Monstera Deliciosa, also known as the Swiss Cheese Plant, is a tropical climbing plant with large, fenestrated leaves, admired for its striking aesthetic and easy care.")
			PlantType.create(name="Zanzibar Gem", nicknames=["ZZ Plant"], thresholds={"soil_moisture": [20, 100], "soil_temperature": [26, 30], "humidity": [50, 60], "temperature": [24, 30], "light_intensity": [800, 900], "barometric_pressure": [960, 1050], "co2": [400, 1000]}, description="The ZZ Plant, or Zamioculcas zamiifolia, is a hardy, low-maintenance houseplant with glossy, dark green leaves, perfect for beginners and thriving in low-light conditions.")
			PlantType.create(name="Strelitzia Nicolai", nicknames=["Birds of Paradise"], thresholds={"soil_moisture": [30, 50], "soil_temperature": [18, 24], "humidity": [50, 70], "temperature": [16, 29], "light_intensity": [800, 900], "barometric_pressure": [960, 1050], "co2": [400, 1000]}, description="The Bird of Paradise, or Strelitzia reginae, is a striking, tropical houseplant known for its lush, banana-like leaves and vibrant, bird-shaped flowers, thriving in bright, indirect light and adding a bold, exotic touch to any space.")

		if "actuator" not in app.config['DB'].list_collection_names():
			Actuator.create('Grow Light', 17)

		if "plant" in app.config['DB'].list_collection_names():
			i2c_manager.start_reading()

	return app
