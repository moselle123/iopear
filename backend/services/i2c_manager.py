import board
import busio
from sensors import SHT31
from sensors import TSL2561

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
	pass

try:
	devices = i2c.scan()

	if devices:
		for address in devices:
			if address == 0x44:
				tempSensor = SHT31(i2c)
				humiditySensor = tempSensor
				print(tempSensor.getTemperature())
				tempSensor.getHumidity()
				print("SHT31 Sensor found at i2c address 0x44")
				
			elif address == 0x70:
				print("Found multiplexor")
				
			elif address == 0x29:
				tsl2561 = TSL2561(i2c)
				print("TSL2561 Sensor found at i2c address 0x29")
	else:
		print("No I2C devices found")
finally:
	i2c.unlock()
