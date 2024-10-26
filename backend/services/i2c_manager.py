import board
import busio
import adafruit_tca9548a
import adafruit_sht31d
import adafruit_tsl2561

class I2CManager:
	def __init__(self, tca9548a_address=0x70):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.tca9548a_address = tca9548a_address

		try:
			self.multiplexer = adafruit_tca9548a.TCA9548A(self.i2c, address=self.tca9548a_address)
			print(f"TCA9548A found at address 0x{self.tca9548a_address:02x}")
		except ValueError:
			print(f"Could not find TCA9548A at address 0x{self.tca9548a_address:02x}")
			exit()

	def scan_channel(self, channel):
		if channel < 0 or channel > 7:
			print("Invalid channel. Must be between 0 and 7.")
			return

		print(f"\nScanning devices on channel {channel}...")
		channel_i2c = self.multiplexer[channel]

		while not channel_i2c.try_lock():
			pass

		try:
			devices = channel_i2c.scan()
			if not devices:
				print("No I2C devices found on this channel.")
				return devices
		finally:
			channel_i2c.unlock()

	def read_sensors(self):
		for channel in range(8):
			devices = self.scan_channel(channel)
			if devices:
				for address in devices:
					if address == 0x44: 
						temp_sensor = adafruit_sht31d.SHT31D(self.multiplexer[channel])
						print(f"SHT31 Sensor found at i2c address 0x44 on channel {channel}")
						print("Temperature:", temp_sensor.temperature)
						print("Humidity:", temp_sensor.relative_humidity)

					elif address == 0x29: 
						tsl2561 = adafruit_tsl2561.TSL2561(self.multiplexer[channel])
						print(f"TSL2561 Sensor found at i2c address 0x29 on channel {channel}")
						print("Light Level:", tsl2561.lux)

					else:
						print(f"Unknown device found at address 0x{address:02x} on channel {channel}")

	def get_temperature(self, channel):
		temp_sensor = adafruit_sht31d.SHT31D(self.multiplexer[channel])
		return temp_sensor.temperature, temp_sensor.relative_humidity

	def get_light_level(self, channel):
		light_sensor = adafruit_tsl2561.TSL2561(self.multiplexer[channel])
		return light_sensor.lux
