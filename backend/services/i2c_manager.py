import board
import busio
import time
import json
import adafruit_sht31d
import adafruit_tsl2561
from adafruit_seesaw.seesaw import Seesaw

class I2CManager:
	def __init__(self):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.sht = adafruit_sht31d.SHT31D(self.i2c)
		time.sleep(3)
		self.tsl = adafruit_tsl2561.TSL2561(self.i2c)
		time.sleep(3)
		self.ss = Seesaw(self.i2c, addr=0x36)
		time.sleep(1)
	
	def read_sensors(self):
		data = {
			'temperature': self.get_temperature_(),
			'humidity': self.get_humidity_(),
			'soil_moisture': self.get_soil_moisture_(),
			'soil_temperature': self.get_soil_temperature_(),
			'lux': self.get_lux_(),
		}
		return data

	def get_temperature_(self):
		return self.sht.temperature

	def get_humidity_(self):
		return self.sht.relative_humidity
	
	def get_soil_moisture_(self):
		return self.ss.moisture_read()

	def get_soil_temperature_(self):
		return self.ss.get_temp()
	
	def get_lux_(self):
		return self.tsl.lux
