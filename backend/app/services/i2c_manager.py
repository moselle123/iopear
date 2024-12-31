import board
import busio
import time
import threading
import logging
import adafruit_sht31d
import adafruit_tsl2561
from adafruit_seesaw.seesaw import Seesaw
from app.services.sensor_registry import SensorRegistry

class I2CManager:
	def __init__(self, app):
		self.app = app
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.last_readings = {}
		self.sht = self.tsl = self.ss  = None

		self.sensors_initialised = False
		self.running = False

	def _initialise_sensors(self):
		try:
			adafruit_sht = adafruit_sht31d.SHT31D(self.i2c)
			self.sht = SensorRegistry.get_sensor("SHT31")
			SensorRegistry.attach_adafruit_instance("SHT31", adafruit_sht)
		except OSError as e:
			print(f"Error initialising SHT31: {e}")
		try:
			adafruit_tsl = adafruit_tsl2561.TSL2561(self.i2c)
			self.tsl = SensorRegistry.get_sensor("TSL2561")
			SensorRegistry.attach_adafruit_instance("TSL2561", adafruit_tsl)
		except OSError as e:
			print(f"Error initialising TSL2561: {e}")
		try:
			adafruit_ss = Seesaw(self.i2c, addr=0x36)
			self.ss = SensorRegistry.get_sensor("SS")
			SensorRegistry.attach_adafruit_instance("SS", adafruit_ss)
		except OSError as e:
			print(f"Error initialising Soil Moisture Sensor: {e}")

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
		last_temp_humidity_read = 0
		last_db_write = 0
		while self.running:
			now = time.time()

			lux = self.get_lux_()
			soil_moisture = self.get_soil_moisture()
			soil_temperature = self.get_soil_temperature_()

			if now - last_temp_humidity_read >= 20:
				temperature = self.get_temperature_()
				humidity = self.get_humidity_()
				last_temp_humidity_read = now
			else:
				temperature = self.last_readings.get('temperature')
				humidity = self.last_readings.get('humidity')

			self.last_readings = {
				'temperature': temperature,
				'humidity': humidity,
				'soil_moisture': soil_moisture,
				'soil_temperature': soil_temperature,
				'lux': lux,
			}
			with self.app.app_context():
				try:
					if now - last_db_write >= 60:
						self.sht.create_reading('temperature', '°C', temperature)
						self.sht.create_reading('humidity', '%', humidity)
						self.tsl.create_reading('lux', 'lx', lux)
						self.ss.create_reading('soil moisture', '%', soil_moisture)
						self.ss.create_reading('soil_temperature', '°C', soil_temperature)
						last_db_write = now
				except Exception as e:
					logging.error(f"Error writing sensor data to the database: {e}")


			time.sleep(interval)

	def get_temperature_(self):
		try:
			return self.sht.adafruit_instance.temperature
		except OSError as e:
			print(f"Error reading temperature: {e}")
			return None

	def get_humidity_(self):
		try:
			return self.sht.adafruit_instance.relative_humidity
		except OSError as e:
			print(f"Error reading humidity: {e}")
			return None

	def get_soil_moisture(self):
		try:
			if self.sensors_initialised:
				return self.ss.adafruit_instance.moisture_read()
			else:
				ss = Seesaw(self.i2c, addr=0x36)
				return ss.moisture_read()

		except OSError as e:
			print(f"Error reading soil moisture: {e}")
			return None

	def get_soil_temperature_(self):
		try:
			return self.ss.adafruit_instance.get_temp()
		except OSError as e:
			print(f"Error reading soil temperature: {e}")
			return None

	def get_lux_(self):
		try:
			return self.tsl.adafruit_instance.lux
		except OSError as e:
			print(f"Error reading lux: {e}")
			return None

	def get_last_readings(self):
		return self.last_readings
