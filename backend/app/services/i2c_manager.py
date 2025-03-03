import board
import busio
import time
import threading
import logging
import adafruit_sht31d
import adafruit_tsl2561
import adafruit_bmp280
import adafruit_scd4x
from adafruit_seesaw.seesaw import Seesaw
from .sensor_registry import SensorRegistry
from .event_manager import EventManager
from app.models import Reading

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class I2CManager:
	def __init__(self, app):
		self.app = app
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.last_readings = {}
		self.SHT31 = self.TSL2561 = self.BMP280 = self.SCD40 = self.SS  = None

		self.sensors_initialised = False
		self.running = False

	def _initialise_sensors(self, sensor_name=None):
		if sensor_name:
			sensor_names = [sensor_name]
		else:
			sensor_names = ["SHT31", "TSL2561", "BMP280", "SCD40", "SS"]
		for name in sensor_names:
			sensor = SensorRegistry.get_sensor(name)
			if not sensor.enabled:
				logger.info(f"Skipping initialization of {name} (disabled by user)")
				continue

			try:
				if name == "SHT31":
					adafruit_instance = adafruit_sht31d.SHT31D(self.i2c)
				elif name == "TSL2561":
					adafruit_instance = adafruit_tsl2561.TSL2561(self.i2c)
					adafruit_instance.gain = 16
					adafruit_instance.integration_time = 402
				elif name == "BMP280":
					adafruit_instance = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=0x76)
				elif name == "SCD40":
					adafruit_instance = adafruit_scd4x.SCD4X(self.i2c)
				elif name == "SS":
					adafruit_instance = Seesaw(self.i2c, addr=0x36)
				else:
					continue

				SensorRegistry.attach_adafruit_instance(name, adafruit_instance)
				setattr(self, name, sensor)
				logger.info(f"Initialized {name}")

			except OSError as e:
				logger.info(f"Error initializing {name}: {e}")

			self.sensors_initialised = True

	def start_reading(self, interval=1):
		if self.sensors_initialised:
			self.running = True
			self.reading_thread = threading.Thread(target=self._read_loop, args=(interval,))
			self.reading_thread.daemon = True
			self.reading_thread.start()

	def stop_reading(self):
		self.running = False
		if self.reading_thread.is_alive():
			self.reading_thread.join()

	def _read_loop(self, interval):
		last_read = 0
		while self.running:
			now = time.time()

			if now - last_read >= 60:
				try:
					with self.app.app_context():
						sensor_data = {}

						if self.SHT31 and self.SHT31.adafruit_instance and self.SHT31.enabled:
							sensor_data['temperature'] = self.get_temperature_()
							sensor_data['humidity'] = self.get_humidity_()
							Reading.create(self.SHT31._id, 'temperature', '°C', sensor_data["temperature"])
							Reading.create(self.SHT31._id, 'humidity', '%', sensor_data["humidity"])
						if self.TSL2561 and self.TSL2561.adafruit_instance and self.TSL2561.enabled:
							sensor_data['light_intensity'] = self.get_lux_()
							Reading.create(self.TSL2561._id, 'light_intensity', 'lx', sensor_data["light_intensity"])
						if self.BMP280 and self.BMP280.adafruit_instance and self.BMP280.enabled:
							sensor_data['barometric_pressure'] = self.get_barometric_pressure_()
							Reading.create(self.BMP280._id, 'barometric_pressure', 'hPa', sensor_data["barometric_pressure"])
						if self.SCD40 and self.SCD40.adafruit_instance and self.SCD40.enabled:
							sensor_data['co2'] = self.get_co2_()
							Reading.create(self.SCD40._id, 'co2', 'ppm', sensor_data["co2"])
						if self.SS and self.SS.adafruit_instance and self.SS.enabled:
							sensor_data['soil_moisture'] = self.get_soil_moisture()
							sensor_data['soil_temperature'] = self.get_soil_temperature_()
							Reading.create(self.SS._id, 'soil_moisture', '%', sensor_data["soil_moisture"], self.SS.calibration)
							Reading.create(self.SS._id, 'soil_temperature', '°C', sensor_data["soil_temperature"])

						self.last_readings = sensor_data
						last_read = now


						try:
							EventManager.check_events(self.last_readings)
							self.app.config['SOCKET_IO'].emit('latest-readings', self.last_readings)
							logger.debug('apparently socket message sent ###################################################################', self.last_readings)
						except Exception as e:
							logger.error(f"Error checking for event instances: {e}")

				except Exception as e:
					logger.error(f"Error writing sensor data to the database: {e}")

			time.sleep(interval)

	def get_temperature_(self):
		if self.SHT31 and self.SHT31.adafruit_instance:
			try:
				return self.SHT31.adafruit_instance.temperature
			except OSError as e:
				logger.error(f"Error reading temperature: {e}")
				return None
		return None

	def get_humidity_(self):
		if self.SHT31 and self.SHT31.adafruit_instance:
			try:
				return self.SHT31.adafruit_instance.relative_humidity
			except OSError as e:
				logger.error(f"Error reading humidity: {e}")
				return None
		return None

	def get_soil_moisture(self):
		try:
			if self.sensors_initialised and self.SS and self.SS.adafruit_instance:
				return self.SS.adafruit_instance.moisture_read()
			else:
				ss = Seesaw(self.i2c, addr=0x36)
				return ss.moisture_read()

		except OSError as e:
			logger.error(f"Error reading soil moisture: {e}")
			return None

	def get_soil_temperature_(self):
		if self.SS and self.SS.adafruit_instance:
			try:
				return self.SS.adafruit_instance.get_temp()
			except OSError as e:
				logger.error(f"Error reading soil temperature: {e}")
				return None
		return None

	def get_lux_(self):
		if self.TSL2561 and self.TSL2561.adafruit_instance:
			try:
				broadband = self.TSL2561.adafruit_instance.broadband
				infrared = self.TSL2561.adafruit_instance.infrared
				return max(0, (0.0304 * broadband) - (0.062 * broadband * (infrared / broadband) ** 1.4)) if broadband > 0 else 0
			except OSError as e:
				logger.error(f"Error reading light intensity: {e}")
				return None
		return None

	def get_co2_(self):
		if self.SCD40 and self.SCD40.adafruit_instance:
			try:
				logger.info(f"Sensor serial number: {self.SCD40.adafruit_instance.serial_number}")
				self.SCD40.adafruit_instance.start_periodic_measurement()
				timeout = time.time() + 2
				while not self.SCD40_instance.data_ready:
					if time.time() > timeout:
						logger.info("CO2 sensor data not ready in time")
						return None
					time.sleep(0.1)
			except OSError as e:
				logger.info(f"Error reading lux: {e}")
				return None
		return None

	def get_barometric_pressure_(self):
		if self.BMP280 and self.BMP280.adafruit_instance:
			try:
				return self.BMP280.adafruit_instance.pressure
			except OSError as e:
				logger.error(f"Error reading barometric pressure: {e}")
				return None
		return None

	def get_last_readings(self):
		return self.last_readings
