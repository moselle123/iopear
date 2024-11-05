import board
import busio
import time
import threading
import adafruit_sht31d
import adafruit_tsl2561
from adafruit_seesaw.seesaw import Seesaw

class I2CManager:
	def __init__(self):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.last_readings = {}

		self.sht = adafruit_sht31d.SHT31D(self.i2c)
		self.tsl = adafruit_tsl2561.TSL2561(self.i2c)
		self.ss = Seesaw(self.i2c, addr=0x36)

		self.running = False
		self.start_reading(10)

	def start_reading(self, interval=1):
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
		while self.running:
			now = time.time()

			lux = self.get_lux_()
			soil_moisture = self.get_soil_moisture_()
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
			time.sleep(interval)

	def get_temperature_(self):
		try:
			return self.sht.temperature
		except OSError as e:
			print(f"Error reading temperature: {e}")
			return None

	def get_humidity_(self):
		try:
			return self.sht.relative_humidity
		except OSError as e:
			print(f"Error reading humidity: {e}")
			return None

	def get_soil_moisture_(self):
		try:
			return self.ss.moisture_read()
		except OSError as e:
			print(f"Error reading soil moisture: {e}")
			return None

	def get_soil_temperature_(self):
		try:
			return self.ss.get_temp()
		except OSError as e:
			print(f"Error reading soil temperature: {e}")
			return None

	def get_lux_(self):
		try:
			return self.tsl.lux
		except OSError as e:
			print(f"Error reading lux: {e}")
			return None

	def get_last_readings(self):
		return self.last_readings
