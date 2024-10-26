import board
import busio
import adafruit_tca9548a
from sensors import SHT31, TSL2561

i2c = busio.I2C(board.SCL, board.SDA)
TCA9548A_ADDRESS = 0x70

try:
    	multiplexor = adafruit_tca9548a.TCA9548A(i2c, address=TCA9548A_ADDRESS)
except ValueError:
	print("Could not find TCA9548A at address 0x" + TCA9548A_ADDRESS)
	exit()

for channel in range(8):
	print("\nScanning devices on channel" + channel + "...")
	i2c = multiplexor[channel]

	while not i2c.try_lock():
		pass

	try:
		devices = i2c.scan()
		
		if devices:
			for address in devices:
				if address == 0x44:
					tempSensor = SHT31(i2c)
					print("SHT31 Sensor found at address 0x44")
					print("Temperature:", tempSensor.getTemperature())
					print("Humidity:", tempSensor.getHumidity())

				elif address == 0x29:
					tsl2561 = TSL2561(i2c)
					print("TSL2561 Sensor found at i2c address 0x29")
					print("Light Level:", tsl2561.getLightIntensity()) 

				else:
					print("Unknown device found at address 0x" + address)
		else:
			print("No I2C devices found on this channel.")

	finally:
		i2c.unlock()

print("Finished.")
