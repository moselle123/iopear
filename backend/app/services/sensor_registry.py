from flask import current_app
from app.models.sensor import Sensor

class SensorRegistry:
	_registry = {}

	@classmethod
	def get_sensor(cls, name):
		if name in cls._registry:
			return cls._registry[name]

		sensor = Sensor.create(name)
		cls._registry[name] = sensor
		return sensor

	@classmethod
	def attach_adafruit_instance(cls, name, adafruit_instance):
		sensor = cls.get_sensor(name)
		if sensor:
			sensor.adafruit_instance = adafruit_instance

	@classmethod
	def update_thresholds(cls, measurement, thresholds):
		if measurement == "humidity" or measurement == "temperature":
			sensor = cls.get_sensor("SHT31")
		elif measurement == "soil moisture" or measurement == "soil temperature":
			sensor = cls.get_sensor("SS")
		elif measurement == "light intensity":
			sensor = cls.get_sensor("TSL2561")

		sensor.update_thresholds(measurement, thresholds)

	@classmethod
	def attach_adafruit_instance(cls, name, adafruit_instance):
		sensor = cls.get_sensor(name)
		if sensor:
			sensor.adafruit_instance = adafruit_instance
