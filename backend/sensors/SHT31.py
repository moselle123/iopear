import adafruit_sht31d

class SHT31():
        def __init__(self, i2c):
                self.sht31 = adafruit_sht31d.SHT31D(i2c)
                
        def getTemperature(self):
                return self.sht31.temperature
        
        def getHumidity(self):
                return self.sht31.humidity