import board
import busio
import adafruit_sht31d
import adafruit_tsl2561
from adafruit_seesaw.seesaw import Seesaw

class I2CManager:
	def __init__(self):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.sht = None
		self.tsl = None
		
		self._initialise_sensors()

	def _initialise_sensors(self):
		print("Scanning I2C bus for devices...")
		while not self.i2c.try_lock():
			pass
		try:
			devices = self.i2c.scan()
			if devices:
				for address in devices:
					try:
					print(f"Device found at address 0x{address:02x}")
					if address == 0x44:
						self.sht = adafruit_sht31d.SHT31D(self.i2c)
						print("SHT31 Sensor initialized at address 0x44.")
					elif address == 0x29:
						self.tsl = adafruit_tsl2561.TSL2561(self.i2c)
						print("TSL2561 Sensor initialized at address 0x29.")
					elif address == 0x36:
						self.ss = Seesaw(self.i2c, addr=0x36)
						print("Soil Moisture Sensor initialized at address 0x36.")
			else:
				print("No I2C devices found.")
		finally:
			self.i2c.unlock()

	def get_temperature(self):
		return self.sht.temperature if self.sht else None

	def get_humidity(self):
		return self.sht.relative_humidity if self.sht else None
	
	def get_soil_moisture(self):
		return self.ss.moisture_read() if self.ss else None

	def get_soil_temperature(self):
		return self.ss.get_temp() if self.ss else None
	
	def get_light_level(self):
		return self.tsl.lux if self.tsl else None
