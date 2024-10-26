import adafruit_tsl2561
class TSL2561():
        def __init__(self, i2c):
                self.tsl2561 = adafruit_tsl2561.TSL2561(i2c)
                
        def getLightIntensity(self):
                return self.tsl3561